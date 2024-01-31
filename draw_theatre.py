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

# colours
GREY = (0.6,0.6,0.6)
BLUE = (0,0,1)
DARKBLUE = (0,0,0.78)
LIGHTBLUE = "#66a3ff"
GREEN = (0,1,0)
RED = (1,0,0)
LIGHTRED = "#ff8080"
WHITE = (1,1,1)
PURPLE = (0.44,0.16,0.39)


def draw_theatre(theatre:Theatre,helper_boxes:bool) -> None:
    # define figure
    fig,axes = plt.subplots(1,1,figsize=(10, 10))
    plt.xlim([0,theatre.MAPWIDTH])
    plt.ylim([0,theatre.MAPHEIGHT])
    # draw helper boxes
    if helper_boxes:
        draw_helper_boxes(theatre)
    # draw units on map
    # blue vehicles
    for vehicle in theatre.blue_vehicles:
        plt.scatter(vehicle.location[0],vehicle.location[1],color=LIGHTBLUE,s=100,marker="o")
    # blue factories
    for factory in theatre.blue_factories:
        plt.scatter(factory.location[0],factory.location[1],color="blue",s=100,marker="H")
    # red vehicles
    for vehicle in theatre.red_vehicles:
        plt.scatter(vehicle.location[0],vehicle.location[1],color=LIGHTRED,s=100,marker="o")
    # red factories
    for factory in theatre.red_factories:
        plt.scatter(factory.location[0],factory.location[1],color="red",s=100,marker="H")
    # blue sams
    for sam in theatre.blue_sams:
        plt.scatter(sam.location[0],sam.location[1],color=LIGHTBLUE,s=100,marker="o")
        circle = plt.Circle(sam.location,sam.radius,color="blue",lw=0.5,fill=False)
        axes.add_patch(circle)
    # red sams
    for sam in theatre.red_sams:
        plt.scatter(sam.location[0],sam.location[1],color=LIGHTRED,s=100,marker="o")
        circle = plt.Circle(sam.location,sam.radius,color="red",lw=0.5,fill=False)
        axes.add_patch(circle)
    # blue airfields
    for airfield in theatre.blue_airfields:
        plt.scatter(airfield.location[0],airfield.location[1],color="blue",s=100,marker="s")
    # red airfields
    for airfield in theatre.red_airfields:
        plt.scatter(airfield.location[0],airfield.location[1],color="red",s=100,marker="D")

    # locations
    blue_points = ([unit.location for unit in theatre.blue_all])
    blue_values = ([unit.value for unit in theatre.blue_all])
    red_points = ([unit.location for unit in theatre.red_all])
    red_values = ([unit.value for unit in theatre.red_all])
    
    # convex hull
    blue_hull = MultiPoint(blue_points).convex_hull
    red_hull = MultiPoint(red_points).convex_hull
    x,y = blue_hull.exterior.xy
    plt.plot(x,y,"b--",lw=0.5)
    x,y = red_hull.exterior.xy
    plt.plot(x,y,"r--",lw=0.5)
    
    # centroid points
    blue_centroid = blue_hull.centroid
    red_centroid = red_hull.centroid
    plt.scatter(blue_centroid.x,blue_centroid.y,color="purple",s=200,marker="*")
    plt.scatter(red_centroid.x,red_centroid.y,color="purple",s=200,marker="*")
    
    # centre of gravity points
    blue_cg_x = sum([point[0] for point in blue_points]) / len(blue_points)
    blue_cg_y = sum([point[1] for point in blue_points]) / len(blue_points)        
    print("blue_cg: ",(blue_cg_x,blue_cg_y))
    plt.scatter(blue_cg_x,blue_cg_y,color="blue",s=200,marker="*")

    blue_wcg_x = sum([unit.location[0]*unit.value for unit in theatre.blue_all]) / sum(blue_values)
    blue_wcg_y = sum([unit.location[1]*unit.value for unit in theatre.blue_all]) / sum(blue_values)
    print("blue weighted cg: ",(blue_wcg_x,blue_wcg_y))
    plt.scatter(blue_wcg_x,blue_wcg_y,color="blue",s=200,marker="*")
    
    red_cg_x = sum([point[0] for point in red_points]) / len(red_points)
    red_cg_y = sum([point[1] for point in red_points]) / len(red_points)        
    print("red_cg: ",(red_cg_x,red_cg_y))
    plt.scatter(red_cg_x,red_cg_y,color="red",s=200,marker="*")
    
    red_wcg_x = sum([unit.location[0]*unit.value for unit in theatre.red_all]) / sum(red_values)
    red_wcg_y = sum([unit.location[1]*unit.value for unit in theatre.red_all]) / sum(red_values)
    print("blue weighted cg: ",(blue_wcg_x,blue_wcg_y))
    plt.scatter(red_wcg_x,red_wcg_y,color="red",s=200,marker="*")
    
    # connecting cgs
    plt.plot((blue_cg_x,red_cg_x),(blue_cg_y,red_cg_y),color="black",linestyle="dashed",lw=0.5)

    # intersection
    line = LineString([(blue_cg_x,blue_cg_y),(red_cg_x,red_cg_y)])
    intersection = blue_hull.intersection(line)
    ic(intersection)
    line2 = affinity.scale(line,3.0,3.0,1.0,"center")
    intersection2 = blue_hull.intersection(line2)
    ic(intersection2)
    coords = list(intersection2.coords)
    ic(coords)
    x,y = line2.xy
    plt.plot(x,y)

    test = split(blue_hull,line2)    # multigeometry
    ic(test)
    test1 = test.geoms[0]   # polygon
    ic(test1)
    x,y = test1.exterior.xy
    plt.plot(x,y)
    test2 = test.geoms[1]   # polygon
    ic(test2)
    x,y = test2.exterior.xy
    plt.plot(x,y)

    test = split(red_hull,line2)    # multigeometry
    ic(test)
    test1 = test.geoms[0]   # polygon
    ic(test1)
    x,y = test1.exterior.xy
    plt.plot(x,y)
    test2 = test.geoms[1]   # polygon
    ic(test2)
    x,y = test2.exterior.xy
    plt.plot(x,y)


    
    
    blue_wcg = np.array([blue_wcg_x,blue_wcg_y])
    red_wcg = np.array([red_wcg_x,red_wcg_y])
    point = np.array([blue_points[0]])

    print("point: ",point)

    dist = np.cross(red_wcg - blue_wcg,point-blue_wcg)/np.linalg.norm(red_wcg - blue_wcg)
    print("dist: ",dist)

    """# examples
    d = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)

    p1=np.array([0,0])
    p2=np.array([10,10])
    p3=np.array([5,7])
    d=np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)
    
    
    
    # make a complex geometry
    input_p = Polygon([[8.80228042602539,60.34198591102353], ... [8.80228042602539,60.34198591102353]])

    # and a complex intersecting line
    input_l = LineString([[8.784770965576172,60.33535977571523], ...[8.82150650024414,60.3352748165263]])

    # union the exterior lines of the polygon with the dividing linestring
    unioned = input_p.boundary.union(input_l)

    # use polygonize geos operator and filter out poygons ouside of origina input polygon
    keep_polys = [poly for poly in polygonize(unioned) if poly.representative_point().within(input_p)]

    # remaining polygons are the split polys of original shape
    MultiPolygon(keep_polys)
    
    
    """


    plt.show()


def draw_helper_boxes(theatre) -> None:
    # blue box
    x_data = [theatre.BLUE_BOX_ABS[0],
                theatre.BLUE_BOX_ABS[0],
                theatre.BLUE_BOX_ABS[0] + theatre.BLUE_BOX_WIDTH,
                theatre.BLUE_BOX_ABS[0] + theatre.BLUE_BOX_WIDTH,
                theatre.BLUE_BOX_ABS[0]]
    y_data = [theatre.BLUE_BOX_ABS[1],
                theatre.BLUE_BOX_ABS[1] + theatre.BLUE_BOX_HEIGHT,
                theatre.BLUE_BOX_ABS[1] + theatre.BLUE_BOX_HEIGHT,
                theatre.BLUE_BOX_ABS[1],
                theatre.BLUE_BOX_ABS[1]]
    plt.plot(x_data,y_data,"b--",lw=0.5)
    # blue airfield box
    x_data = [theatre.BLUE_BOX_ABS[0] + theatre.BLUE_AIRFIELD_BOX_REL[0],
                theatre.BLUE_BOX_ABS[0] + theatre.BLUE_AIRFIELD_BOX_REL[0],
                theatre.BLUE_BOX_ABS[0] + theatre.BLUE_AIRFIELD_BOX_REL[0] + theatre.BLUE_AIRFIELD_BOX_WIDTH,
                theatre.BLUE_BOX_ABS[0] + theatre.BLUE_AIRFIELD_BOX_REL[0] + theatre.BLUE_AIRFIELD_BOX_WIDTH,
                theatre.BLUE_BOX_ABS[0] + theatre.BLUE_AIRFIELD_BOX_REL[0]]
    y_data = [theatre.BLUE_BOX_ABS[1] + theatre.BLUE_AIRFIELD_BOX_REL[1],
                theatre.BLUE_BOX_ABS[1] + theatre.BLUE_AIRFIELD_BOX_REL[1] + theatre.BLUE_AIRFIELD_BOX_HEIGHT,
                theatre.BLUE_BOX_ABS[1] + theatre.BLUE_AIRFIELD_BOX_REL[1] + theatre.BLUE_AIRFIELD_BOX_HEIGHT,
                theatre.BLUE_BOX_ABS[1] + theatre.BLUE_AIRFIELD_BOX_REL[1],
                theatre.BLUE_BOX_ABS[1] + theatre.BLUE_AIRFIELD_BOX_REL[1]]
    plt.plot(x_data,y_data,"b--",lw=0.5)
    # blue lorad N box
    x_data = [theatre.BLUE_BOX_ABS[0] + theatre.BLUE_LORAD_N_BOX_REL[0],
                theatre.BLUE_BOX_ABS[0] + theatre.BLUE_LORAD_N_BOX_REL[0],
                theatre.BLUE_BOX_ABS[0] + theatre.BLUE_LORAD_N_BOX_REL[0] + theatre.LORAD_BOX_WIDTH,
                theatre.BLUE_BOX_ABS[0] + theatre.BLUE_LORAD_N_BOX_REL[0] + theatre.LORAD_BOX_WIDTH,
                theatre.BLUE_BOX_ABS[0] + theatre.BLUE_LORAD_N_BOX_REL[0]]
    y_data = [theatre.BLUE_BOX_ABS[1] + theatre.BLUE_LORAD_N_BOX_REL[1],
                theatre.BLUE_BOX_ABS[1] + theatre.BLUE_LORAD_N_BOX_REL[1] + theatre.LORAD_BOX_HEIGHT,
                theatre.BLUE_BOX_ABS[1] + theatre.BLUE_LORAD_N_BOX_REL[1] + theatre.LORAD_BOX_HEIGHT,
                theatre.BLUE_BOX_ABS[1] + theatre.BLUE_LORAD_N_BOX_REL[1],
                theatre.BLUE_BOX_ABS[1] + theatre.BLUE_LORAD_N_BOX_REL[1]]
    plt.plot(x_data,y_data,"b--",lw=0.5)
    # blue lorad S box
    x_data = [theatre.BLUE_BOX_ABS[0] + theatre.BLUE_LORAD_S_BOX_REL[0],
                theatre.BLUE_BOX_ABS[0] + theatre.BLUE_LORAD_S_BOX_REL[0],
                theatre.BLUE_BOX_ABS[0] + theatre.BLUE_LORAD_S_BOX_REL[0] + theatre.LORAD_BOX_WIDTH,
                theatre.BLUE_BOX_ABS[0] + theatre.BLUE_LORAD_S_BOX_REL[0] + theatre.LORAD_BOX_WIDTH,
                theatre.BLUE_BOX_ABS[0] + theatre.BLUE_LORAD_S_BOX_REL[0]]
    y_data = [theatre.BLUE_BOX_ABS[1] + theatre.BLUE_LORAD_S_BOX_REL[1],
                theatre.BLUE_BOX_ABS[1] + theatre.BLUE_LORAD_S_BOX_REL[1] + theatre.LORAD_BOX_HEIGHT,
                theatre.BLUE_BOX_ABS[1] + theatre.BLUE_LORAD_S_BOX_REL[1] + theatre.LORAD_BOX_HEIGHT,
                theatre.BLUE_BOX_ABS[1] + theatre.BLUE_LORAD_S_BOX_REL[1],
                theatre.BLUE_BOX_ABS[1] + theatre.BLUE_LORAD_S_BOX_REL[1]]
    plt.plot(x_data,y_data,"b--",lw=0.5)
    # red box
    x_data = [theatre.RED_BOX_ABS[0],
                theatre.RED_BOX_ABS[0],
                theatre.RED_BOX_ABS[0] + theatre.RED_BOX_WIDTH,
                theatre.RED_BOX_ABS[0] + theatre.RED_BOX_WIDTH,
                theatre.RED_BOX_ABS[0]]
    y_data = [theatre.RED_BOX_ABS[1],
                theatre.RED_BOX_ABS[1] + theatre.RED_BOX_HEIGHT,
                theatre.RED_BOX_ABS[1] + theatre.RED_BOX_HEIGHT,
                theatre.RED_BOX_ABS[1],
                theatre.RED_BOX_ABS[1]]
    plt.plot(x_data,y_data,"r--",lw=0.5)
    # red airfield box
    x_data = [theatre.RED_BOX_ABS[0] + theatre.RED_AIRFIELD_BOX_REL[0],
                theatre.RED_BOX_ABS[0] + theatre.RED_AIRFIELD_BOX_REL[0],
                theatre.RED_BOX_ABS[0] + theatre.RED_AIRFIELD_BOX_REL[0] + theatre.RED_AIRFIELD_BOX_WIDTH,
                theatre.RED_BOX_ABS[0] + theatre.RED_AIRFIELD_BOX_REL[0] + theatre.RED_AIRFIELD_BOX_WIDTH,
                theatre.RED_BOX_ABS[0] + theatre.RED_AIRFIELD_BOX_REL[0]]
    y_data = [theatre.RED_BOX_ABS[1] + theatre.RED_AIRFIELD_BOX_REL[1],
                theatre.RED_BOX_ABS[1] + theatre.RED_AIRFIELD_BOX_REL[1] + theatre.RED_AIRFIELD_BOX_HEIGHT,
                theatre.RED_BOX_ABS[1] + theatre.RED_AIRFIELD_BOX_REL[1] + theatre.RED_AIRFIELD_BOX_HEIGHT,
                theatre.RED_BOX_ABS[1] + theatre.RED_AIRFIELD_BOX_REL[1],
                theatre.RED_BOX_ABS[1] + theatre.RED_AIRFIELD_BOX_REL[1]]
    plt.plot(x_data,y_data,"r--",lw=0.5)
    # red lorad N box
    x_data = [theatre.RED_BOX_ABS[0] + theatre.RED_LORAD_N_BOX_REL[0],
                theatre.RED_BOX_ABS[0] + theatre.RED_LORAD_N_BOX_REL[0],
                theatre.RED_BOX_ABS[0] + theatre.RED_LORAD_N_BOX_REL[0] + theatre.LORAD_BOX_WIDTH,
                theatre.RED_BOX_ABS[0] + theatre.RED_LORAD_N_BOX_REL[0] + theatre.LORAD_BOX_WIDTH,
                theatre.RED_BOX_ABS[0] + theatre.RED_LORAD_N_BOX_REL[0]]
    y_data = [theatre.RED_BOX_ABS[1] + theatre.RED_LORAD_N_BOX_REL[1],
                theatre.RED_BOX_ABS[1] + theatre.RED_LORAD_N_BOX_REL[1] + theatre.LORAD_BOX_HEIGHT,
                theatre.RED_BOX_ABS[1] + theatre.RED_LORAD_N_BOX_REL[1] + theatre.LORAD_BOX_HEIGHT,
                theatre.RED_BOX_ABS[1] + theatre.RED_LORAD_N_BOX_REL[1],
                theatre.RED_BOX_ABS[1] + theatre.RED_LORAD_N_BOX_REL[1]]
    plt.plot(x_data,y_data,"r--",lw=0.5)
    # red lorad S box
    x_data = [theatre.RED_BOX_ABS[0] + theatre.RED_LORAD_S_BOX_REL[0],
                theatre.RED_BOX_ABS[0] + theatre.RED_LORAD_S_BOX_REL[0],
                theatre.RED_BOX_ABS[0] + theatre.RED_LORAD_S_BOX_REL[0] + theatre.LORAD_BOX_WIDTH,
                theatre.RED_BOX_ABS[0] + theatre.RED_LORAD_S_BOX_REL[0] + theatre.LORAD_BOX_WIDTH,
                theatre.RED_BOX_ABS[0] + theatre.RED_LORAD_S_BOX_REL[0]]
    y_data = [theatre.RED_BOX_ABS[1] + theatre.RED_LORAD_S_BOX_REL[1],
                theatre.RED_BOX_ABS[1] + theatre.RED_LORAD_S_BOX_REL[1] + theatre.LORAD_BOX_HEIGHT,
                theatre.RED_BOX_ABS[1] + theatre.RED_LORAD_S_BOX_REL[1] + theatre.LORAD_BOX_HEIGHT,
                theatre.RED_BOX_ABS[1] + theatre.RED_LORAD_S_BOX_REL[1],
                theatre.RED_BOX_ABS[1] + theatre.RED_LORAD_S_BOX_REL[1]]
    plt.plot(x_data,y_data,"r--",lw=0.5)
    
    


