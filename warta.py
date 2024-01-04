from OSMPythonTools.api import Api
import geopy.distance
from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt 


R = 6373.0

api = Api()
river = api.query('relation/3272339')
riverSegmentsNumber = len(river.members())
print(riverSegmentsNumber)
totalDistance = 0.0
totalDistance2 = 0.0
lat = []
lon = []
segmentsLength = []
latOfFirstPointInSegment = []
lonOfFirstPointInSegment = []


def calculateDistanceOfSegment(coordinates):
    distance = 0.0
    
    for x in range(0,(len(coordinates)-1)):
        distance = distance + geopy.distance.geodesic(coordinates[x], coordinates[x+1]).km
    latOfFirstPointInSegment.append(coordinates[0][0])
    lonOfFirstPointInSegment.append(coordinates[0][1])
    return distance
    
def calculateDistanceOfSegment2(coordinates):
    distance = 0.0
    for x in range(0,(len(coordinates)-1)):
        lat1 = radians(float(coordinates[x][0]))
        lon1 = radians(float(coordinates[x][1]))
        lat2 = radians(float(coordinates[x+1][0]))
        lon2 = radians(float(coordinates[x+1][1]))
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = distance + R * c
        
        lat.append(coordinates[x][0])
        lon.append(coordinates[x][1])
        
    return distance



for segment in river.members():
    if(segment.id() == 6124894):
        break
    segmentsLength.append(totalDistance)
    distanceForSegment = calculateDistanceOfSegment(segment.geometry()["coordinates"])
    distanceForSegment2 = calculateDistanceOfSegment2(segment.geometry()["coordinates"])
    totalDistance =  totalDistance + distanceForSegment 
    totalDistance2 = totalDistance2 + distanceForSegment2
    
    print("distance of segment " + str(segment.id()) + " = " + str(distanceForSegment)+ " another method = "+ str(distanceForSegment2))
  
print(totalDistance)
print(totalDistance2)

fig, ax = plt.subplots()  
ax.scatter(lat, lon)
for i, txt in enumerate(segmentsLength):
    ax.annotate(str(round(txt,2)), (latOfFirstPointInSegment[i], lonOfFirstPointInSegment[i]))

plt.show()
