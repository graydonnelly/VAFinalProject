#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(tidyverse)
library(lubridate)
library(sp)
# 
# ## (re)install spatial packages from source
# install.packages(c("rgeos", "sf", "sp"), type = "source")
# 
# ## rgdal requires some additional configuration to build correctly:
# ##   based on http://stackoverflow.com/a/26836125/1380598
# install.packages("rgdal", type = "source",
#                  configure.args = c("--with-proj-include=/usr/local/include",
#                                     "--with-proj-lib=/usr/local/lib"))
# library(rgdal)
# 
# 
# library(sf)
# 
# trymap<-  st_read("cb_2018_us_cd116_500k.shp")
# 
# plot(st_geometry(trymap))
# 
# streetmap<-  st_read("Abila.shp", stringAsFactors = FALSE, sf_column_name = "geometry") 
# 
# streetmap<-  st_read("Abila.shp")
# 
# %>% 
#   st_make_valid() %>% 
#   st_set_crs(4326)
# 
# plot(st_geometry(streetmap))
# 
# 
# st_crs(streetmap)
# #try
# streetmap=streetmap%>% filter(str_length(geometry))
# 

#gps <- read_csv("Downloads/gps.csv", col_types = cols(Timestamp = col_datetime(format = "%m/%d/%Y %H:%M:%S"), 
#                                                      id = col_integer()))
load("gps.RData")
#gps = gps %>% mutate(Timestamp = round_date(Timestamp, unit= "minutes"))
gps
#save(gps,file="gps.RData")
# Define UI for application that draws a histogram
ui <- fluidPage(

    
    # Application title
    titlePanel("Geolocation plot"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            numericInput("id",
                        "Id:",
                        min = min(gps$id),
                        max = max(gps$id),
                        value = 35),
            sliderInput("Timestamp",
                        "Timestamp",
                        min= min(gps$Timestamp),
                        max = max(gps$Timestamp),
                        value= range(gps$Timestamp))
            
        ),

        # Show a plot of the generated distribution
        mainPanel(
           plotOutput("distPlot")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {

    output$distPlot <- renderPlot({
        gps_filtered <- gps %>% filter(id == input$id, Timestamp < input$Timestamp)
        # generate bins based on input$bins from ui.R
        ggplot(gps_filtered, aes(x=long, y=lat))+
            coord_quickmap()+
            geom_point() +
            labs(title= paste("This is Id number",input$id ))
    })
}

# Run the application 
shinyApp(ui = ui, server = server)
