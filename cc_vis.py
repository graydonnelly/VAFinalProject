import pandas as pd
from business_coords import coords
from graphics import *
import math
from business_view import show_info
import tkinter as tk
import time
import datetime

#get the cc data
cc_data = pd.read_csv(r'./Data/cc_data.csv')
#cc_data = pd.to_datetime(cc_data['timestamp'])

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

#make a list of circles for each location
circles = dict(coords)
for location in coords.keys():
    c1=Circle(coords[location], 10)
    c1.setFill('red')
    circles[location] = c1

#draws the circles based on the timeframe
def draw_circles(start_time, end_time):

    #undraw everything else
    for item in circles.values():
        item.undraw()

    #filter by time
    df_new = cc_data[(pd.to_datetime(cc_data['timestamp']) > str(start_time)) & (pd.to_datetime(cc_data['timestamp']) < str(end_time))]

    #draw the circles based on total money spent
    for location in circles.keys():
        df_location = df_new[df_new['location'] == location]
        total_spent = df_location['price'].sum()
        circles[location] = Circle(coords[location], math.sqrt(total_spent)/3)
        circles[location].setFill('red')
        circles[location].draw(win1)

draw_circles(datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 30, 0, 0))

#setup the messages for when hovering over a location
hover_messages = dict(coords)
for location in coords.keys():
    hover_messages[location] = Text(coords[location], location)

#setup the rectangles over the dates
rectangles = []
for i in range(0,15):
    r1 = Rectangle(Point(i/15*2739,1534),Point((i+1)/15*2739,1640))
    r1.setFill('blue')
    if i==0:
        r1.setFill('red')
    rectangles.append(r1)

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

#list of datetimes
dates = [datetime.datetime(2014,1,6,0,0), datetime.datetime(2014,1,7,0,0), datetime.datetime(2014,1,8,0,0), datetime.datetime(2014,1,9,0,0), datetime.datetime(2014,1,10,0,0), datetime.datetime(2014,1,11,0,0), datetime.datetime(2014,1,12,0,0), datetime.datetime(2014,1,13,0,0), datetime.datetime(2014,1,14,0,0), datetime.datetime(2014,1,15,0,0), datetime.datetime(2014,1,16,0,0), datetime.datetime(2014,1,17,0,0), datetime.datetime(2014,1,18,0,0), datetime.datetime(2014,1,19,0,0), datetime.datetime(2014,1,20,0,0)]

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
                if x > i/15*2739 and x < (i+1)/15*2739:
                    rectangles[i].draw(win1)
                    if i == 0:
                        draw_circles(datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 30, 0, 0))
                    else:
                        draw_circles(dates[i-1], dates[i])
                    for rect in rectangles:
                        if rect != rectangles[i]:
                            rect.undraw()

input("press ENTER")