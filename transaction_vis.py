import pandas as pd
from business_coords import coords
from graphics import *
import math
from business_view import show_info
import tkinter as tk
import time
import datetime
import pickle

#list of datetimes
dates = ["all_time", datetime.datetime(2014,1,6,0,0), datetime.datetime(2014,1,7,0,0), datetime.datetime(2014,1,8,0,0), datetime.datetime(2014,1,9,0,0), datetime.datetime(2014,1,10,0,0), datetime.datetime(2014,1,11,0,0), datetime.datetime(2014,1,12,0,0), datetime.datetime(2014,1,13,0,0), datetime.datetime(2014,1,14,0,0), datetime.datetime(2014,1,15,0,0), datetime.datetime(2014,1,16,0,0), datetime.datetime(2014,1,17,0,0), datetime.datetime(2014,1,18,0,0), datetime.datetime(2014,1,19,0,0), datetime.datetime(2014,1,20,0,0)]

#get the dictionary containing necessary data
data = pickle.load(open("transaction_data_dict.pkl", "rb"))

current_date_number = None
current_mode = "cc" #either cc or loyalty

#draw the window and the image
#767, 1534
win1 = GraphWin("Purchases", 1369.5,820)
win1.setCoords(0,1640,2739,0)
myImage = Image(Point(1369.5,767), './Data/MC2-tourist.png')
myImage.draw(win1)

#draw the time bar
Line(Point(0,1534),Point(2739,1534)).draw(win1)
for i in range(1,15):
    Line(Point(i*(2739/15),1534), Point(i*(2739/15),1640)).draw(win1)
    if i == 1:
        Text(Point(i*(2739/15)-91.3,1587), "ALL TIME").draw(win1)
    else:
        Text(Point(i*(2739/15)-91.3,1587), "1/{}".format(str(i+4))).draw(win1)
Text(Point(15*(2739/15)-91.3,1587), "1/19").draw(win1)

#draw the credit card vs loyalty switch
rec1 = Rectangle(Point(1600,25), Point(2000,125))
rec1.setOutline("black")
rec1.draw(win1)
rec2 = Rectangle(Point(2000,25), Point(2400,125))
rec2.setOutline("black")
rec2.draw(win1)
tex1 = Text(Point(1800,75), "SHOW CREDIT CARD DATA").draw(win1)
tex2 = Text(Point(2200,75), "SHOW LOYALTY DATA").draw(win1)


#make a list of circles for each location
circles = dict(coords)
for location in coords.keys():
    c1=Circle(coords[location], 10)
    c1.setFill('red')
    circles[location] = c1

#draws the circles based on the timeframe
def update_circles():
    
    if current_date_number != None:
        print("HI")
        #get date
        date = dates[current_date_number]
        #undraw everything else
        for item in circles.values():
            item.undraw()

        #draw the circles based on total money spent
        for location in circles.keys():
            circles[location] = Circle(coords[location], math.sqrt(data[location][str(date)][current_mode]["total_spent"])/3)
            circles[location].setFill('red')
            circles[location].draw(win1)

#setup the messages for when hovering over a location
hover_messages = dict(coords)
for location in coords.keys():
    hover_messages[location] = Text(coords[location], location)


#gets the mouse wherever it is hovering
def motion(event):

    x, y = event.x*2, event.y*2
    #print('{}, {}'.format(x, y))

    #draw/undraw the hover messages
    if y<1534:
    
        drawn = False
        for location in coords.keys():
                #distance formula    
                
                if math.sqrt((x-coords[location].getX())**2+(y-coords[location].getY())**2) < circles[location].getRadius()+5:
                    hover_messages[location].draw(win1)
                    drawn = True
        if drawn == False:
            for value in hover_messages.values():
                value.undraw()
                

win1.bind('<Motion>', motion)



#setup the rectangles over the dates
date_rectangles = []
for i in range(0,15):
    r1 = Rectangle(Point(i/15*2739,1534),Point((i+1)/15*2739,1640))
    r1.setFill('blue')
    if i==0:
        r1.setFill('red')
    date_rectangles.append(r1)

#setup mode rectangles
mode_rect_cc = Rectangle(Point(1600,25), Point(2000,125))
mode_rect_cc.setFill('yellow')
mode_rect_cc.draw(win1)
mode_rect_loyalty = Rectangle(Point(2000,25), Point(2400,125))
mode_rect_loyalty.setFill('yellow')


#gets the clicks
while True:

    mouse = win1.checkMouse()
    if mouse != None:

        x = mouse.getX()
        y = mouse.getY()

        #open a window showing specific information related to that location, coded in show_info
        for location in coords.keys():
            #distance formula
            if math.sqrt((x-coords[location].getX())**2+(y-coords[location].getY())**2) < 10:
                show_info(location)

        #for when the user clicks a date
        if y>1534:
            for i in range(0,15):

                if current_date_number != i:

                    if x > i/15*2739 and x < (i+1)/15*2739:

                        for rect in date_rectangles:
                            if rect != date_rectangles[i]:
                                rect.undraw()

                        date_rectangles[i].draw(win1)
                        current_date_number = i
                        update_circles()

                    

        #for when the user clicks the cc vs loyalty toggle
        if 25 < y < 125:

            if 1600 < x < 2000:
                if current_mode != "cc":
                    current_mode = "cc"
                    mode_rect_cc.draw(win1)
                    mode_rect_loyalty.undraw()
                    update_circles()
                
            if 2000 < x < 2400:
                if current_mode != "loyalty":
                    current_mode = "loyalty"
                    mode_rect_loyalty.draw(win1)
                    mode_rect_cc.undraw()
                    update_circles()


input("press ENTER")