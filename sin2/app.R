# title: "GPS Data"
# author: "Sofia Baptista, Liwen Xu"
# date: "Last updated on `r Sys.Date()`"

library(shiny)
library(shinydashboard)
library(dashboardthemes)
library(tidyverse)
library(lubridate)
library(sp)
library(rsconnect)
library(png)
library(ggpubr)
library(htmltools)

load("gps.RData")
#gps

#x <- c(1, 5, 4, 9, 0)

#gpsVector <- as.vector(unique(gps$id))

# library(raster)
# shape_A <- shapefile("Abila.shx")

require(rgdal)
shape_A <- readOGR(dsn = "Abila.shp", layer = "Abila")
#shape_K <- readOGR(dsn = "Kronos_Island.shp", layer = "Kronos_Island")

#img <- readPNG("MC2-tourist.png")

theme1 <- theme(panel.border = element_blank(), panel.grid.major = element_blank(),
                panel.grid.minor = element_blank(), axis.line = element_line(colour = "grey"), panel.background = element_rect(fill = "white", colour = "white"), legend.position = "bottom")

ui <- navbarPage(
    # Application title
    title = "Ablia Map",
    
    tabPanel("Map",
             titlePanel("Geolocation of Employees"),
             
             # Sidebar with a slider input for number of bins
             sidebarLayout(
                 sidebarPanel(
                     #Allows control panel to stay fixed while scrolling
                     style = "position:fixed;width:inherit",
                     width = 3,
                     selectInput("id",
                                 "Id:",
                                 sort(unique(gps$id)),
                                 35,
                                 multiple = TRUE),
                     sliderInput("Timestamp",
                                 "Timestamp",
                                 min= min(gps$Timestamp),
                                 max = max(gps$Timestamp),
                                 value= range(gps$Timestamp)) #fix so lower bound is actually lower
                     
                 ),
                 
                 # Show a plot of the generated distribution
                 mainPanel(
                     width = 9,
                     div(style = 'overflow: visible',
                         plotOutput("distPlot" , height="auto", width = "auto"))
                 )
             )
    ),
    
    tabPanel(
        "About", htmlOutput("Sampletext")
    )
)#ui



server <- function(input, output, session) {
    
    output$Sampletext<- renderText({
        HTML(
            "<p><b>Our code</b></p>
         <p>Description of our diagram</br>
         Description of our diagram</p>
         <a href='https://github.com/isidonnelly/VAFinalProject'>Github repository</a>"
        )
    })
    
    output$distPlot <- renderPlot({
        gps_filtered <- gps %>% filter(id %in% input$id, between(Timestamp, left = min(input$Timestamp), right = max(input$Timestamp)))
        # generate bins based on input$bins from ui.R
        ggplot(data = gps_filtered, aes(x=long, y=lat, color = factor(id)))+
            #background_image(img) +
            coord_quickmap()+
            geom_point(alpha = .2)+
            #Gives their latest/current location
            geom_point(data = (gps_filtered %>%
                                   group_by(id) %>%
                                   arrange(desc(gps_filtered$Timestamp)) %>%
                                   slice(1) %>%
                                   ungroup()), 
                       aes(x = long, y = lat),
                       shape = 18,
                       size = 8) +
            #geom_point(color = factor(id)) +
            #labs(legend.position = "bottom", legend.title = "ID: ") +
            xlim(24.844, 24.906) +
            ylim(36.047, 36.091) +
            guides(color = guide_legend (title = "ID Number:")) +
            geom_polygon(data = shape_A, aes(x = long, y = lat, group = group), colour = "black", fill = NA) +
            theme1 
        # +
        #     scale_x_continuous(limits = c(24.844, 24.906), expand = c(0, 0)) +
        #     scale_y_continuous(limits = c(36.047, 36.091), expand = c(0, 0))
    }, 
    height = function() {
        session$clientData$output_distPlot_width
    })
}#Server

# Run the application
shinyApp(ui = ui, server = server)