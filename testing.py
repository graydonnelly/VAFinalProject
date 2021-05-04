import pandas as pd
from business_coords import coords
from graphics import *
import math
from business_view import show_info
import tkinter as tk

cc_data = pd.read_csv(r'./Data/cc_data.csv')

locations = cc_data.location.unique()

#767, 1534
win1 = GraphWin("Purchases", 1369.5,800)
win1.setCoords(0,1600,2739,0)
myImage = Image(Point(1369.5,767), './Data/MC2-tourist.png')
myImage.draw(win1)

for point in coords.values():
    c1=Circle(point, 10)
    c1.setFill('red')
    c1.draw(win1)

import graphics
root = graphics._root

while True:

    x = root.winfo_rootx()
    y = root.winfo_pointery()
    print(x)

    key = win1.checkKey()
    mouse = win1.checkMouse()
    
    if mouse != None:
        for location in coords.keys():
            #distance formula
            if math.sqrt((mouse.getX()-coords[location].getX())**2+(mouse.getY()-coords[location].getY())**2) < 10:
                show_info(location)

input("press ENTER")