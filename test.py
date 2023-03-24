import math

def calculate_coordinates_along_line(long_1, lat_1, long_2, lat_2, num_points):
    # Calculate the distance between the two points
    R = 6371 # Radius of the earth in km
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
    coordinates = [(long_1 + i * delta_long, lat_1 + i * delta_lat) for i in range(num_points)]

    return coordinates
coordinates = calculate_coordinates_along_line(127.1489424997404, 37.447236415879765,127.1489667143757, 37.44723122736077,6)
for i in range(len(coordinates)):
    print("{" + "lat:{},lon:{}".format(coordinates[i][1],coordinates[i][0])+"},")