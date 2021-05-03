import pandas as pd
from business_coords import coords
from graphics import *

cc_data = pd.read_csv(r'./Data/cc_data.csv')

locations = cc_data.location.unique()

print(locations)
print(len(locations))

win1 = GraphWin("Purchases", 1369.5,767)
win1.setCoords(0,1534,2739,0)
myImage = Image(Point(1369.5,767), './Data/MC2-tourist.png')
myImage.draw(win1)

for point in coords.values():
    c1=Circle(point, 10)
    c1.setFill('red')
    c1.draw(win1)

input("press ENTER")