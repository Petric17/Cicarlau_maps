# Import libraries
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import cartopy
import cartopy.crs as ccrs
import cartopy.mpl.gridliner as gridliner
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.patches import ConnectionPatch
from shapely.geometry import box

# Load Data 
boundary_path = r'C:\Users\petrica.s\geospatial_project\geo_work\data\raw\UAT\uat_boundary.gpkg'
boundary = gpd.read_file(boundary_path).to_crs(epsg=3857)
minx, miny, maxx, maxy = boundary.total_bounds

romania_path = r"C:\Users\petrica.s\geospatial_project\geo_work\data\raw\geoBoundaries-ROU-ADM0-all\geoBoundaries-ROU-ADM0.shp"
romania = gpd.read_file(romania_path).to_crs(epsg=3857)

# Setup Figure 
fig = plt.figure(figsize=(15, 15), dpi=300)
ax = plt.axes(projection=ccrs.Mercator()) 
ax.set_extent([minx - 1000, maxx + 1000, miny - 1000, maxy + 1000], crs=ccrs.Mercator())

 #Map Layering 
try:
    
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=13, alpha=0.7, attribution=False)
    ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery, zoom=13, attribution=False)
    world = box(-2e7, -2e7, 2e7, 2e7)
    mask = gpd.GeoDataFrame(geometry=[world], crs=boundary.crs).overlay(boundary, how='difference')
    mask.plot(ax=ax, facecolor='white', alpha=0.6, zorder=5)

except Exception as e:
    print(f"Connection Warning: Basemap could not load. Error: {e}")

# Romania Inset 
inset_ax = fig.add_axes([0.08, 0.68, 0.22, 0.22], projection=ccrs.Mercator())

romania.plot(ax=inset_ax, facecolor='#f9f9f9', edgecolor='black', linewidth=0.6)
try:
    ctx.add_basemap(inset_ax, 
                    source=ctx.providers.Esri.WorldTopoMap, 
                    zoom=6, 
                    attribution=False, 
                    alpha=0.9, 
                    zorder=1)
except Exception:
    ctx.add_basemap(instet_ax, source=ctx.providers.Esri.WorldTerrain, zoom=6, attribution=False)
boundary.plot(ax=inset_ax, color='red', markersize=5, zorder=10)
inset_ax.set_axis_off()

#Miniature boundary

boundary.plot(ax=inset_ax, facecolor='red', edgecolor='red', linewidth=1.2, zorder=10)
inset_ax.set_axis_off()

# Connection Lines 

for corner_x, corner_y in [(minx, maxy), (minx, miny)]: 
    con = ConnectionPatch(xyA=(corner_x, corner_y), xyB=(corner_x, corner_y), 
                          coordsA="data", coordsB="data",
                          axesA=inset_ax, axesB=ax, 
                          color="gray", alpha=0.6, linewidth=1, linestyle='--')
    fig.add_artist(con)

# Styling & Grid

gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='white', alpha=0.3, linestyle='--')
gl.top_labels = gl.right_labels = False
gl.xlabel_style = {'size': 10, 'color': 'gray'}
gl.ylabel_style = {'size': 10, 'color': 'gray'}
gl.xformatter = cartopy.mpl.gridliner.LONGITUDE_FORMATTER
gl.yformatter = cartopy.mpl.gridliner.LATITUDE_FORMATTER

# Main Boundary 

boundary.plot(ax=ax, facecolor='none', edgecolor="#00FF00", linewidth=3, zorder=15)

#Title


plt.suptitle("Cicârlău, Maramureș", fontsize=24, y=0.94, fontweight='bold')
ax.set_title("Localizare Administrativă și Context Geografic", fontsize=14, color='gray', pad=25)

# North Arrow 

ax.text(0.95, 0.95, 'N', transform=ax.transAxes, fontsize=14, fontweight='bold', color='white', ha='center', zorder=20)
ax.arrow(0.95, 0.90, 0, 0.04, transform=ax.transAxes, head_width=0.015, width=0.01, 
         length_includes_head=True, facecolor='white', edgecolor='white', zorder=20)

# Scale bar

scale_bar = ScaleBar(1, location='lower right', box_alpha=0.5, border_pad=1)
ax.add_artist(scale_bar)

#save figure

plt.savefig(r'C:\Users\petrica.s\geospatial_project\geo_work\data\processed\final_map.png', dpi=300, bbox_inches='tight')
