import sqlite3
from shapely.geometry import Point, Polygon
import os
from quantized_mesh_tile import decode
from quantized_mesh_tile.global_geodetic import GlobalGeodetic
import time

first = time.perf_counter()

conn = sqlite3.connect('terrain_database.db')
cursor = conn.execute("SELECT file_path, x, y, z FROM selected")

geodetic = GlobalGeodetic(True)
bounds = None
polygon_vertices = [(127.14698761544736, 37.448164855223666), (127.14695560200964, 37.44816122976021),                    (127.14694592433774, 37.44822061702554), (127.1469845712283, 37.44822169252189)]
poly = Polygon(polygon_vertices)

tiles = []

for row in cursor:
    [path,x,y,z] = row
    bounds = geodetic.TileBounds(x, y, z)
    tile = decode(path, bounds)
    uv1 = [(v[0], v[1]) for v in tile.getVerticesCoordinates()]
    indexes = [i for i, v in enumerate(uv1) if Point(v[0], v[1]).within(poly)]
    height = tile._quantizeHeight(13)
    tile.h = [height if i in indexes else h for i, h in enumerate(tile.h)]
    tiles.append((tile, path))

cursor.close()

with conn:
    for tile, path in tiles:
        tile.toBytesIO()
        os.remove(path)
        tile.toFile(path)

t_time = time.perf_counter() - first
print(f"Time taken for tile is {t_time}")
