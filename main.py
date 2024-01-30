import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import contextily as ctx

# Read data from Excel file
file_path = 'AirQualityData.xlsx'  # Replace with the actual file path
df = pd.read_excel(file_path)

# Create a GeoDataFrame from the DataFrame
geometry = [Point(xy) for xy in zip(df["Long"], df["Lat"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Read a basemap of India (you need to have the necessary shapefiles)
india = gpd.read_file('india_ds.shp')  # Replace with the actual file path

# Plot the India map with AQI data
fig, ax = plt.subplots(figsize=(12, 12))
india.plot(ax=ax, color='lightgray', edgecolor='k')
gdf.plot(ax=ax, marker='o', color='red', markersize=50, alpha=0.5)
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
plt.title("Spread of AQI Data in India")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
