"""
This file was made to show specific info about individual businesses.
"""
from graphics import *
from business_coords import coords
import pandas as pd
import datetime
pd.options.mode.chained_assignment = None

#enter any keyboard key to break before closing window
def show_info(location):

    #get the cc data
    cc_data = pd.read_csv(r'./Data/cc_data.csv')

    #draw the window
    win1 = GraphWin(location, 1369.5,800)
    win1.setCoords(0,1600,2739,0)
    win1.setBackground("linen")

    #selected location
    spec_loc = cc_data[cc_data['location'] == location]

    #total money spent at selected location in full timeframe 
    cc_spent = spec_loc['price'].sum()
    cc_spent = str(cc_spent)

    #sort by employee cc
    spec_loc.drop("location",axis=1,inplace=True)
    ind_num = spec_loc.sort_values(by=["last4ccnum"]).to_csv(index=False)
    #ind_num.drop("location",axis=1,inplace=True)
    num = Text(Point(500, 800),  ind_num )
    num.setTextColor('Black')
    num.draw(win1)

    #individual employees that visited location
    spec_loc.drop_duplicates(subset = 'last4ccnum', keep = 'last', inplace = True)
    spec_loc.drop("timestamp",axis=1,inplace=True)
    spec_loc.drop("price",axis=1,inplace=True)
    ind_cust = spec_loc.sort_values(by=["last4ccnum"]).to_csv(index=False)
    cust = Text(Point(1350,500), ind_cust)
    cust.setTextColor('Black')
    cust.draw(win1)
    
    #rectangle to cover extra at the top
    cover = Rectangle(Point(0,0), Point(1600,230))
    cover.setFill('linen')
    cover.setOutline('linen')
    cover.draw(win1)

    #rectangle boxes
    box1 = Rectangle(Point(80,230), Point(850,1590))
    box1.draw(win1)

    box2 = Rectangle(Point(1100,230), Point(1700,1590))
    box2.draw(win1)

    box3 = Rectangle(Point(1950,230), Point(2550,1590))
    box3.draw(win1)

    #titles
    info = Text(Point(1500,50),"Information for " + location)
    info.setTextColor('Black')
    info.setSize(25)
    info.draw(win1)

    info1 = Text(Point(1200,103), "At " + location + ", according to the credit card data, employees spent " + cc_spent + " in total over the course of two weeks.")
    info1.setTextColor('Black')
    info1.setSize(13)
    info1.draw(win1)

    info2 = Text(Point(500,170), "A list of transactions at " + location + "\nUse up/down arrows to scroll through")
    info2.setSize(13)
    info2.setTextColor('Black')
    info2.draw(win1)
    
    info3 = Text(Point(1400,170), "Individuals customers at " + location + "\nUse left/right arrows to scroll through")
    info3.setSize(13)
    info3.setTextColor('Black')
    info3.draw(win1)

    info4 = Text(Point(2300,170), "Look up individual's activies by entering cc number" + "\nClick any non-scroll keyboard key to view entry box" + "\nClick anywhere on window to start/clear search" + "\nEnter a 0 into entry box and press anywhere on window before exiting")
    info4.setTextColor('Black')
    info4.setSize(13)
    info4.draw(win1)

    #ind_sum = ind_spend['price'].sum()
    #ind2 = Text(Point(2100,1200), ind_sum)
    #ind2.setTextColor('Black')
    #ind2.draw(win1)

    #'scroll' through values in box1 and box2
    while True:
        key = win1.getKey ()
        #print ('key=', key)
        if key == ('Up'):
            num.move ( 0, 30 )
        elif key == ('Down') :
            num.move ( 0, -30 )
        elif key == ('Left') :
            cust.move ( 0, 30 )
        elif key == ('Right') :
            cust.move( 0, -30 )
        else:
            break

    #look up individuals and their transactions
    while True:
        inputBox = Entry(Point(2300, 260), 20)
        inputBox.setFill('grey')
        inputBox.draw(win1)
        
        win1.getMouse()
        inputStr = inputBox.getText()
        inputInt = int(inputStr)

        if (inputStr == '0'):

            endText = Text(Point(2425,340), "Breaking out!\nThank you!")
            endText.setTextColor('Red')
            endText.setSize(15)
            endText.draw(win1)
    
            break
        else:
            #individual employee and how much they spent at location over 2 weeks
            ind_loc = cc_data[cc_data['location'] == location]
            ind_loc.drop('location',axis=1,inplace=True)
            
            ind_spend = ind_loc[ind_loc['last4ccnum'].eq(inputInt)]
            ind_spend = ind_spend.to_csv(index=False)
            ind1 = Text(Point(2250,500), ind_spend)
            ind1.setTextColor('Black')
            ind1.draw(win1)

            win1.getMouse()
            
            cover1 = Rectangle(Point(1955,245), Point(2540,1580))
            cover1.setFill('linen')
            cover1.setOutline('linen')
            cover1.draw(win1)
