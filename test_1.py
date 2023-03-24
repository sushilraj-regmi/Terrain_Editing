from quantized_mesh_tile.global_geodetic import GlobalGeodetic
from quantized_mesh_tile import decode,encode
import quantized_mesh_tile
from io import BytesIO
from quantized_mesh_tile.terrain import TerrainTile


file = 'tiles1\\21\\3578521\\1484878.terrain'
geodetic = GlobalGeodetic(True)
[z, x, y] = [21,3578521,1484878]
[west, south, east, north] = bounds = geodetic.TileBounds(x, y, z)


tile = decode(file,bounds)


hei = [None] * len(tile.h)

for i in range(int(len(tile.h))):
   
    hei[i] = tile._dequantizeHeight(tile.h[i])



for i in range(0,1,2):
    hei[i]=11
tile.header['minimumHeight'] = 10
for i in range(0,1,2):
    tile.h[i] = tile._quantizeHeight(hei[i])

new = hei

for i in range(int(len(tile.h))):
    if i in [0,1,2]:
        new[i] = tile._dequantizeHeight(tile.h[i])

for i in range(len(tile.h)):
    tile.h[i]=tile._quantizeHeight(new[i])
last= [None] * len(tile.h)
for i in range(int(len(tile.h))):
    
    last[i] = tile._dequantizeHeight(tile.h[i])

print(last)