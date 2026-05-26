import numpy as np
import os
import cartopy.crs as ccrs
import rasterio as rio
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import scipy
import pykdtree as kdtree


#load the NIR and red bands

nir_path = r"C:\Users\petrica.s\geospatial_project\geo_work\data\processed\nir_band\S2A_MSIL2A_20241128T092331_N0511_R093_T34TFT_20241128T122153.SAFE\GRANULE\L2A_T34TFT_A049282_20241128T092331\IMG_DATA\R10m\T34TFT_20241128T092331_B08_10m.jp2"   
red_path = r"C:\Users\petrica.s\geospatial_project\geo_work\data\processed\nir_band\S2A_MSIL2A_20241128T092331_N0511_R093_T34TFT_20241128T122153.SAFE\GRANULE\L2A_T34TFT_A049282_20241128T092331\IMG_DATA\R10m\T34TFT_20241128T092331_B04_10m.jp2"

print(f"Loading geospatial data...")

with rio.open(nir_path) as src:
    nir = src.read(1).astype('float32')
    bounds = src.bounds
    img_extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
    utm_crs = ccrs.UTM(zone=34, southern_hemisphere=False)

with rio.open(red_path) as src:
    red = src.read(1).astype('float32')

print(f"Geospatial data loaded successfully.")

#calculate the NDVI
print(f"Calculating NDVI...")

ndvi = (nir - red) / (nir + red + 1e-10)
ndvi = np.clip(ndvi, -1, 1)
print(f"NDVI calculated successfully.")

#Create a custom colormap

colors = ['#8b4513', '#fffacd', '#32cd32', '#006400']
n_bins = 100 
cmap = 'lush_veg'
custom_cmap = LinearSegmentedColormap.from_list(cmap, colors, N=n_bins)

#Plotting with cartopy

fig = plt.figure(figsize=(15,12))
ax = plt.axes(projection=utm_crs)


#Zoom in on the area of interes
#calculate a 10km x 10km box around the center

zoom_x = (bounds.left + bounds.right) / 2
zoom_y = (bounds.bottom + bounds.top) / 2
buffer = 7000 
ax.set_extent([zoom_x - buffer, zoom_x + buffer, zoom_y - buffer, zoom_y + buffer], crs=utm_crs)

img = ax.imshow(ndvi, cmap=custom_cmap, extent=img_extent, transform=utm_crs, origin='upper')

# Gridlines

gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
gl.top_labels = False
gl.right_labels = False

# Colorbar

cbar = plt.colorbar(img, ax=ax, orientation='vertical', shrink=0.7, pad=0.02)
cbar.set_label('Vegetation Health Index (NDVI)', fontsize=12)

plt.title('NDVI Map - Cicârlău (Nov 2024)', fontsize=16, pad=20)

#Save

output_folder = r"C:\Users\petrica.s\geospatial_project\geo_work\Maps"
os.makedirs(output_folder, exist_ok=True)
output_path = os.path.join(output_folder, "Cicarlau_NDVI.png")