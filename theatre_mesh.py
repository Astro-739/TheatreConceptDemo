import random
import math
from icecream import ic
from shapely.geometry import Point,Polygon,LineString,MultiPoint,GeometryCollection
from shapely.geometry import box
from shapely.ops import split
from shapely import affinity
import matplotlib.pyplot as plt
import numpy as np

from create_theatre import Theatre


def create_threatre_mesh(theatre:Theatre) -> None:
    
    points = []
    
    points1 = ([unit.location for unit in theatre.blue_airfields])
    points2 = ([unit.location for unit in theatre.blue_factories])
    points3 = ([unit.location for unit in theatre.blue_sams])
    points4 = ([unit.location for unit in theatre.blue_vehicles])
    points5 = ([unit.location for unit in theatre.blue_all])

    points = points1 + points2 + points3 + points4
    print("points: ",points)
    print("all points: ",points5)
    
    hull = MultiPoint(points5).convex_hull
    x,y = hull.exterior.xy
    plt.plot(x,y)
    buffer = hull.buffer(50)
    a,b = buffer.exterior.xy
    plt.plot(a,b)
    centroid = hull.centroid
    print("centroid: ",centroid)
    
    plt.scatter(centroid.x,centroid.y,color="purple",s=200,marker="*")
        
    polygon1 = Polygon(points)
    x,y = polygon1.exterior.xy
    plt.plot(x,y)

    bounds = polygon1.bounds
    print("bounds: ",bounds)
    buffer = polygon1.buffer(100)
    a,b = buffer.exterior.xy
    plt.plot(a,b)
    
    box1 = box(*bounds)
    a,b = box1.exterior.xy
    plt.plot(a,b)
    buffer1 = box1.buffer(100)
    a,b = buffer1.exterior.xy
    plt.plot(a,b)
    
    
    
    
    
    
    plt.show()



