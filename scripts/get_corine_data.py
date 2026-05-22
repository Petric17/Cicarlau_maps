#required libraries

import geopandas as gpd
from pystac_client import Client
import odc.stac 
import matplotlib.pyplot as plt


#load the Cicarlau boundary data

boundary = gpd.read_file(r'C:\Users\petrica.s\geospatial_project\geo_work\data\raw\UAT\uat_boundary.gpkg')
bbox = boundary.total_bounds

#Connect to the Copernicus stac API 

print(f"Searching for Sentinel-2 data...")

client = Client.open("https://earth-search.aws.element84.com/v1")

#search for the corine land cover data

search = client.search(
    collections=["sentinel-2-l2a"],
    bbox=bbox,
    datetime="2024-06-01/2024-09-30",
    query={"eo:cloud_cover": {"lt": 10}}
)
items = list(search.get_items())

if len(items) == 0:
    print(" No clear images found. Try changing the date range!")
else:
    print(f" Found {len(items)} clear images. Downloading...")

#Load the data

data = odc.stac.load(items[:1], bbox=bbox, bands=["red", "nir08"], resolution=10)

#Calculate the NDVI

red = data.red.astype(float)
nir = data.nir08.astype(float)
ndvi = (nir - red) / (nir + red)

#Visualise 

print(" Plotting your vegetation map...")
plt.figure(figsize=(10, 10))
ndvi.isel(time=0).plot(cmap="RdYlGn", vmin=0, vmax=1)
plt.title("Vegetation Density (NDVI) from Sentinel-2")
plt.show()



