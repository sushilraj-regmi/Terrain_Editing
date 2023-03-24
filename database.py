import pickle
from shapely.geometry import Point, Polygon
import os
import re
import sqlite3
from quantized_mesh_tile.global_geodetic import GlobalGeodetic
from quantized_mesh_tile import decode, encode
from quantized_mesh_tile.terrain import TerrainTile
geodetic = GlobalGeodetic(True)
# define the regular expression to extract boundary values


# create an empty dictionary to store the data
data_dict = {}

# traverse through all the nested folders to access the ".terrain" files
for root, dirs, files in os.walk('tiles1'):
    for file in files:
        if file.endswith('.terrain'):
            file_path = os.path.join(root, file)
            # print(file_path)
            # extract the boundary values from the file
            components = file_path.split(os.sep)

# Extract the z, x, and y values from the components
            z = int(components[1])
            x = int(components[2])
            y, _ = os.path.splitext(components[3])
            y = int(y)
            # print(f'z={z}, x={x}, y={y}')

            [west, south, east, north] = bounds = geodetic.TileBounds(x, y, z)
            tile = decode(file_path, bounds)
            entry = {
                'bounds': [(tile._west, tile._north), (tile._east, tile._north), (tile._east, tile._south), (tile._west, tile._south)],
                'file_path': file_path
            }

            # # Add the dictionary to the list of dictionaries for this tile
            data_dict.setdefault((z, x, y), []).append(entry)
            # print(data_dict)


# create a SQLite database
conn = sqlite3.connect('terrain_database.db')

# create a table with columns for x, y, z, bounds, and file path
conn.execute('''CREATE TABLE terrainData1
             (x INTEGER, y INTEGER, z INTEGER, bounds BLOB, file_path TEXT);''')

# example dictionary


# insert the data into the table using an SQL insert statement
for key, value in data_dict.items():
    z, x, y = key
    bounds = pickle.dumps(value[0]['bounds'])
    file_path = value[0]['file_path']
    conn.execute("INSERT INTO terrainData1 (z, x, y, bounds, file_path) VALUES (?, ?, ?, ?, ?)",
                 (z, x, y, bounds, file_path))

# commit the changes and close the database connection
conn.commit()
conn.close()
