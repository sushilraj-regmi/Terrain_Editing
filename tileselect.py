import sqlite3
import pickle
import math
from shapely.geometry import Point, Polygon
import time 
first = time.perf_counter()
# polygon vertices coordinates
polygon = [(127.14698761544736, 37.448164855223666), (127.14695560200964, 37.44816122976021),
           (127.14694592433774, 37.44822061702554), (127.1469845712283, 37.44822169252189)]
polygon1 = polygon.copy()


def calculate_coordinates_along_line(long_1, lat_1, long_2, lat_2, num_points):
    # Calculate the distance between the two points
    R = 6371  # Radius of the earth in km
    dLat = math.radians(lat_2-lat_1)
    dLon = math.radians(long_2-long_1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat_1)) \
        * math.cos(math.radians(lat_2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    total_distance = R * c

    # Determine the distance between each point
    segment_distance = total_distance / (num_points - 1)

    # Calculate the offset in latitude and longitude for each point
    delta_lat = (lat_2 - lat_1) / total_distance * segment_distance
    delta_long = (long_2 - long_1) / total_distance * segment_distance

    # Calculate the coordinates of each point
    coordinates = [(long_1 + i * delta_long, lat_1 + i * delta_lat)
                   for i in range(num_points)]

    return coordinates[1:-1]


for i in range(len(polygon)):
    if i != len(polygon)-1:
        cc = calculate_coordinates_along_line(
            polygon[i][0], polygon[i][1], polygon[i+1][0], polygon[i+1][1], 6)

        for i in range(len(cc)):
            polygon1.append(cc[i])
    if i == len(polygon)-1:
        dd = calculate_coordinates_along_line(
            polygon[i][0], polygon[i][1], polygon[0][0], polygon[0][1], 6)
        # polygon1.append()

        for i in range(len(dd)):
            polygon1.append(dd[i])

# print(len(polygon1))
# for i in range(len(polygon1)):
#     print("{" + "lat:{},lon:{}".format(polygon1[i][1],polygon1[i][0])+"},")
# create a SQLite database connection
conn = sqlite3.connect('terrain_database.db')
zxy = []
# retrieve the bounds and file path values from the database using a SELECT statement
cursor = conn.execute("SELECT bounds, file_path,x,y,z FROM terrainData1")
conn.execute("DELETE FROM selected ")
new_file_path = []
# iterate over the result set and check if any polygon vertices are inside the bounds
for row in cursor:
    bounds = pickle.loads(row[0])
    # if z > 15:
   
    file_path, z,x, y = row[1],row[4],row[2], row[3]
    for i in (polygon1):
        # print(i)
        p = Point(i)
        polygon2 = Polygon(bounds)
        if p.within(polygon2):
            if file_path not in new_file_path:
                new_file_path.append(file_path)
                zxy.append((z, x, y))
                # conn.execute('''CREATE TABLE selected
                #      (z INTEGER, x INTEGER, y INTEGER, file_path TEXT);''')
                conn.execute("INSERT INTO selected (z, x, y, file_path) VALUES (?, ?, ?, ?)",
                             (z, x, y, file_path))
            # print(bounds)


# close the database connection
conn.commit()
conn.close()
t_time = time.perf_counter()- first
print(f"Time taken for tile selection is{t_time}")
