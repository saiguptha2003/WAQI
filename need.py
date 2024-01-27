import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import numpy as np
import contextily as ctx

# Read data from Excel file
file_path = 'AirQualityData.xlsx'  # Replace with the actual file path
df = pd.read_excel(file_path)

# Create a GeoDataFrame from the DataFrame
geometry = [Point(xy) for xy in zip(df["Long"], df["Lat"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Create a grid for interpolation
x_min, x_max = gdf.bounds["minx"].min(), gdf.bounds["maxx"].max()
y_min, y_max = gdf.bounds["miny"].min(), gdf.bounds["maxy"].max()
grid_size = 100
x = np.linspace(x_min, x_max, grid_size)
y = np.linspace(y_min, y_max, grid_size)
x, y = np.meshgrid(x, y)

# Interpolate AQI values using Inverse Distance Weighting (IDW)
coordinates = gdf[["Long", "Lat"]].values
values = gdf["AQI"].values
aqi_values_idw = griddata(coordinates, values, (x, y), method='cubic', fill_value=np.nan)

# Create a GeoDataFrame for IDW interpolation results
interpolation_df = pd.DataFrame({
    'Longitude': x.flatten(),
    'Latitude': y.flatten(),
    'AQI_IDW': aqi_values_idw.flatten()
})
interpolation_geometry = [Point(xy) for xy in zip(interpolation_df["Longitude"], interpolation_df["Latitude"])]
gdf_idw = gpd.GeoDataFrame(interpolation_df, geometry=interpolation_geometry)

# Plot the entire India map with AQI IDW interpolation
fig, ax = plt.subplots(figsize=(12, 12))
india = gpd.read_file('india_ds.shp')  # Replace with the actual file path to India shapefile
india.plot(ax=ax, color='red', edgecolor='k')
gdf_idw.plot(ax=ax, column='AQI_IDW', cmap='viridis', legend=True, vmin=gdf["AQI"].min(), vmax=gdf["AQI"].max())
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
plt.title("Spread of AQI Data in India with IDW Interpolation")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
