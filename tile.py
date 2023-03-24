from quantized_mesh_tile.global_geodetic import GlobalGeodetic
from quantized_mesh_tile import decode,encode
import quantized_mesh_tile
from io import BytesIO
from quantized_mesh_tile.terrain import TerrainTile
import os
import struct
import pyproj
from shapely.geometry import Point, Polygon
import sqlite3





conn = sqlite3.connect('terrain_database.db')
cursor = conn.execute("SELECT file_path,x,y,z FROM selected")

for row in cursor:
    geodetic = GlobalGeodetic(True)
    [z, x, y] = [row[3],row[1],row[2]]
    [west, south, east, north] = bounds = geodetic.TileBounds(x, y, z)
    path = row[0]

    tile = decode(path,bounds)



    uv1 = [None] * (len(tile.getVerticesCoordinates()))
    for i in range(len(tile.getVerticesCoordinates())):
        uv1[i]=(tile.getVerticesCoordinates()[i][0],tile.getVerticesCoordinates()[i][1]) 
# print(uv1)
    indexes= []
    heightValue = 14
    
    polygon_vertices = [(127.14698761544736, 37.448164855223666),(127.14695560200964, 37.44816122976021), (127.14694592433774, 37.44822061702554),(127.1469845712283, 37.44822169252189)]
    poly = Polygon(polygon_vertices)
    for i in range(len(uv1)):
        p1 = Point(uv1[i][0], uv1[i][1])
        if p1.within(poly):
            indexes.append(i)

# print(indexes)
# for i in range(len(tile.getVerticesCoordinates())):
#       if i in indexes:
#             print("{" + "lat:{},lon:{}".format(tile.getVerticesCoordinates()[i][1],tile.getVerticesCoordinates()[i][0])+"},")
    # if heightValue<tile.header['minimumHeight']:
    #     tile.header['minimumHeight'] = heightValue  
    # if heightValue>tile.header['maximumHeight']:
    #     tile.header['maximumHeight']=heightValue

    height = tile._quantizeHeight(heightValue)
    
    print(path)
    print(height)
    for i in range((len(tile.h))):
        if i in indexes: 

            tile.h[i] = height
            
            # print(path)
            
            
              

    tile.toBytesIO()
    os.remove(path)
    tile.toFile(path)
      


