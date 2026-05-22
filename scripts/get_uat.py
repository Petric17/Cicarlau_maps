#required libraries

import geopandas as gpd
import rasterio as rio
import osmnx as ox
import matplotlib.pyplot as plt
import shapely as shp
import os 



#load the uat boundary data

uat_location = 'Cicârlău, Romania'
output_loc = r'C:\Users\petrica.s\geospatial_project\geo_work\data\raw\UAT'

if not os.path.exists(output_loc):
    os.makedirs(output_loc)
    print(f"Created directory at {output_loc}")

print(f"Searching for data for {uat_location}")


boundary = ox.geocode_to_gdf(uat_location)

file_path = os.path.join(output_loc, f"uat_boundary.gpkg")

boundary.to_file(file_path, driver='GPKG')

print(f"Boundary data saved to {file_path}")





