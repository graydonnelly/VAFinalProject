# title: "GPS Data"
# author: "Sofia Baptista, Liwen Xu"
# date: "Last updated on `r Sys.Date()`"

library(shiny)
library(tidyverse)
library(lubridate)
library(sp)
library(rsconnect)
library(png)
library(ggpubr)
library(htmltools)

#Reading in Data
load("gps.RData")
carAssn <- read.csv("car-assignments.csv")
carAssn <- carAssn %>% select(CarID, LastName, FirstName, CurrentEmploymentType, CurrentEmploymentTitle)

carAssn <- read.csv("car-assignments.csv")
carAssn <- carAssn %>%
    rename(id = CarID)
monster <- gps %>%
    full_join(carAssn)

require(rgdal)
shape_A <- readOGR(dsn = "Abila.shp", layer = "Abila")

#Setting the theme
theme1 <- theme(panel.border = element_blank(), 
                panel.grid.major = element_blank(),
                panel.grid.minor = element_blank(), 
                axis.line = element_line(colour = "grey"), 
                panel.background = element_rect(fill = "white", colour = "white"), 
                legend.position = "bottom",
                legend.text = element_text(size = 20),
                legend.title = element_text(size = 25),
                axis.text = element_text(size = 13),
                axis.title = element_text(size = 18))
#UI for Shiny
ui <- navbarPage(
    # Application title
    title = "Ablia Map",
    
    tabPanel("Map",
             titlePanel("Employee Vehicle Locations"),
             
             # Sidebar with a slider input for number of bins
             sidebarLayout(
                 sidebarPanel(
                     #Allows control panel to stay fixed while scrolling
                     style = "position:fixed;width:inherit",
                     width = 3,
                     selectInput("id",
                                 "Car ID:",
                                 sort(unique(monster$id)),
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
             ),
             
             fluidRow(column(width = 12), tableOutput("idtext"))
    ),
    
    tabPanel(
        "About", htmlOutput("Sampletext"), tableOutput("Tableid")
    )
)#ui


#Server for shiny
server <- function(input, output, session) {
    
    output$Sampletext<- renderText({
        HTML(
            "<p><b>About this Tool</b></p>
            <p>This graph is made using GPS tracking data about Kronos citizens provided by GAStech. This is intended for use by Kronos law enforcement.</br>
            <p></p>
            The large diamonds on the map indicate a car's location at the latest time selected, or the car's \"current\" location for that window of time. At the very bottom of the map there is a legend indicating which color corresponds to which car ID. Individuals are identified by an their car ID number assigned to them by their employer who has also provided their first and last name, employment category, and title. Below is a list of the correspondences between ID number and Name. ID numbers above 100 correspond to trucks and could have been driven by any truck driver during the period.</p>
            <p> </p>
            <p>To look at our code and source data please visit our 
            <a href='https://github.com/isidonnelly/VAFinalProject'>Github repository</a> </p>
            <p><i>Data source:
            <a href='https://vast-challenge.github.io/2021/'>VAST Challenge 2021 - Mini-Challenge 2</a> </i> </p>"
        )
    })
    
    output$Tableid <- renderTable({carAssn})
    
    output$idtext <- renderTable({
        idInformation <- monster %>% 
            select(id, LastName, FirstName, CurrentEmploymentType, CurrentEmploymentTitle) %>%
            unique() %>%
            filter(id %in% input$id)
        #paste("Name of id you selected:", Firstname$idInformation, Lastname$idInformation)
        
    })
    
    output$distPlot <- renderPlot({
        gps_filtered <- monster %>% filter(id %in% input$id, between(Timestamp, left = min(input$Timestamp), right = max(input$Timestamp)))
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

#library(rsconnect)
#deployApp(appName="sin2", account="sofiabaptista")
#rsconnect::deployApp('C:/Users/sbapt/Desktop/Smith/DATA CHALLENGES/final/MC2/MC2/MC2/sin2')