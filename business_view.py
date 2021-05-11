"""
This file was made to show specific info about individual businesses.
"""
from graphics import *
from business_coords import coords
import pandas as pd

#must break by pressing '.' first before closing window
def show_info(location):
    #get the cc data
    cc_data = pd.read_csv(r'./Data/cc_data.csv')

    #draw the window
    win1 = GraphWin(location, 1369.5,800)
    win1.setCoords(0,1600,2739,0)
    win1.setBackground("linen")

    #selected location
    spec_loc = cc_data[cc_data.location == location]

    #sort by employee cc
    cc_num = spec_loc['last4ccnum'].to_csv(index=False)
    ind = spec_loc.sort_values(by=["last4ccnum"]).to_csv(index=False)
    ind = str(ind)

    #cluster of employee actions at location thus shown together
    num = Text(Point(500, 800),  ind )
    num.setTextColor('Black')
    num.draw(win1)

    #rectangle to cover extra at the top
    cover = Rectangle(Point(0,0), Point(800,175))
    cover.setFill('linen')
    cover.setOutline('linen')
    cover.draw(win1)

    #main title 
    info = Text(Point(1500,50),"Information for " + location)
    info.setTextColor('Black')
    info.setSize(25)
    info.draw(win1)

    #transaction view title
    info2 = Text(Point(500,160), "A list of transactions at " + location)
    info2.setTextColor('Black')
    info2.draw(win1)

    #total money spent at selected location in full timeframe 
    cc_spent = spec_loc['price'].sum()
    cc_spent = str(cc_spent)

    info = Text(Point(1200,130), "At " + location + ", according to the credit card data, employees spent " + cc_spent + " in total over the course of two weeks.")
    info.setTextColor('Black')
    info.draw(win1)

    #'scroll' through transactions
    while True:
        key = win1.getKey ()
        print ( 'key=', key)
        if key == ('Up'):
            num.move ( 0, 20 )
        elif key == ('Down') :
            num.move ( 0, -20 )
        #must break first before closing window
        elif key == 'period':
            break
