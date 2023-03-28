from quantized_mesh_tile.global_geodetic import GlobalGeodetic
from quantized_mesh_tile import decode,encode
import quantized_mesh_tile
from io import BytesIO
from quantized_mesh_tile.terrain import TerrainTile
import os
from past.utils import old_div
file = 'tiles1\\21\\3578521\\1484878.terrain'
geodetic = GlobalGeodetic(True)
[z, x, y] = [21,3578521,1484878]
[west, south, east, north] = bounds = geodetic.TileBounds(x, y, z)


tile = decode(file,bounds)



print(tile.h)
# print((tile.header))

# hei = [None]*len(tile.h)

# for i in range(len(tile.h)):
#     hei[i] = tile._dequantizeHeight(tile.h[i])

# print(hei)
# qhei = [None]*len(tile.h)
# for i in range(len(tile.h)):
#     qhei[i] = tile._quantizeHeight(hei[i])

# print(qhei)
# height = tile._quantizeHeight(11)
# tile.h[0] = height
tile.header['minimumHeight'] = 12.40833854675293
# print(tile.h[0])
# print(tile.header)
tile.toBytesIO()
os.remove(file)
tile.toFile(file)

# new_path = 'edited.terrain'
# geodetic = GlobalGeodetic(True)
# [z, x, y] = [21,3578521,1484878]
# [west, south, east, north] = bounds = geodetic.TileBounds(x, y, z)


# new_tile = decode(new_path,bounds)
# print(new_tile.h)
# real = new_tile._dequantizeHeight(tile.h[0])
# print(real)