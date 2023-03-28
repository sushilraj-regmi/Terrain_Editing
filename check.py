from quantized_mesh_tile.global_geodetic import GlobalGeodetic
from quantized_mesh_tile import decode,encode
import quantized_mesh_tile
from io import BytesIO
from quantized_mesh_tile.terrain import TerrainTile
import os
from past.utils import old_div
file = 'tiles1\\21\\3578521\\1484878_orig.terrain'  # I have copy pasted the file so not to replace original file
replace_file = 'tiles1\\21\\3578521\\1484878.terrain'
geodetic = GlobalGeodetic(True)
[z, x, y] = [21,3578521,1484878]
[west, south, east, north] = bounds = geodetic.TileBounds(x, y, z)


tile = decode(file,bounds)

print("HEADER\n---------------\n")
print(tile.header)
print("\n---------------\n")
print("HEIGHTS\n---------------\n")
print(tile.h)
print("\n---------------\n")

hei = [None]*len(tile.h)

for i in range(len(tile.h)):
    hei[i] = tile._dequantizeHeight(tile.h[i])

print("HEI\n---------------\n")
print(hei)
print("\n---------------\n")
qhei = [None]*len(tile.h)
for i in range(len(tile.h)):
    qhei[i] = tile._quantizeHeight(hei[i])

print("QHEI\n---------------\n")
print(qhei)
print("\n---------------\n")

orig_minheight = tile.header['minimumHeight']
orig_maxheight = tile.header['maximumHeight']

new_minheight = 12.0
new_maxheight = 14.5

ENCODING_MAX = 32767.0

##EDITING 

tile.header['minimumHeight'] = new_minheight
tile.header['maximumHeight'] = new_maxheight

# tile.toBytesIO()
# os.remove(replace_file)
# tile.toFile(replace_file)

# tile = decode(replace_file,bounds)

print("EDITED HEADER\n---------------\n")
print(tile.header)
print("\n---------------\n")

edited_qhei = [None]*len(tile.h)

for i in range(len(qhei)):
    edited_qhei[i] = int( ( ((orig_minheight - new_minheight)*ENCODING_MAX) + ((orig_maxheight - orig_minheight)*qhei[i]) ) / (new_maxheight - new_minheight) )

print("EDITED QHEI\n---------------\n")
print(edited_qhei)
print("\n---------------\n")

edited_hei = [None]*len(tile.h)

for i in range(len(tile.h)):
    edited_hei[i] = tile._dequantizeHeight(edited_qhei[i])

print("EDITED HEI\n---------------\n")
print(edited_hei)
print("\n---------------\n")



