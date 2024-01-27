import geopandas as gpd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import numpy as np

# Load the air quality data
gdf = gpd.read_file('AirQualityData.xlsx', sheet_name='AirQualityData')

# Extract relevant columns
points = gdf[['Long', 'Lat']].values
values = gdf['AQI'].values

# Create a grid for interpolation
grid_x, grid_y = np.mgrid[min(gdf['Long']):max(gdf['Long']):1000j, min(gdf['Lat']):max(gdf['Lat']):1000j]

# Perform IDW interpolation
grid_z = griddata(points, values, (grid_x, grid_y), method='cubic')

# Create a GeoDataFrame for the grid
grid_gdf = gpd.GeoDataFrame({'geometry': gpd.points_from_xy(grid_x.flatten(), grid_y.flatten()), 'Interpolated_AQI': grid_z.flatten()})

# Plot the original data points
ax = gdf.plot(column='AQI', cmap='viridis', markersize=5, legend=True)

# Plot the interpolated surface
grid_gdf.plot(column='Interpolated_AQI', cmap='viridis', ax=ax, linewidth=0.8, linestyle=':', alpha=0.7)

plt.title('Air Quality Index (AQI) - IDW Interpolation')
plt.show()
