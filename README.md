# The Kronos Incident 

We built our system based on the data from Mini-Challenge 2 of the 2021 VAST challenge, which contains the geospatial and transaction data of GAStech employees over a two-week period. Its purpose is to assist the officers of the Abila Police Department in their investigation of the disappearance of GAStech employees through the visualization of employee activities in order to locate places and dates of interest.

## The Visualizations 

Officers running transaction_vis.py will be able to view a visualization of employee credit and loyalty card transactions. A map of Abila displays where GAStech employees spent money and how much they spent there in total. The officer using this visualization will be able to select a certain date from the bottom of the map, showing transaction information for the chosen date. On the top right corner, the officer can select whether they wish to view a visualization of the credit card data or the loyalty data. They are also able to click on a specific location, which will load a pop-up window. 

This pop-up window is created by business_view.py, which the user will not need to run. This new window allows displays information regarding the chosen location's customers and transactions. The first window will be a list of the information of all transactions at that location, sorted by credit card number and then date. The second window lists the individual credit cards that were used at the location, and the third window allows the officer to input an individual credit card number to see that employee's transactions. 

A visualization for the geolocation data will allow the officer to view the routes taken by GAStech employees, search by employee ID, and move through time with a slider to observe daily routines. This visualization is live at https://sofiabaptista.shinyapps.io/sin2/

## Dependencies needed:
Users will not need any dependencies to interact with the geolocation data visualization. 
### Python dependencies
- [pandas](https://pandas.pydata.org/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)
- [graphics](https://github.com/isidonnelly/VAFinalProject/blob/main/graphics.py) (included in file)

