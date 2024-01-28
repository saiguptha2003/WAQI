import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from scipy.interpolate import griddata
import contextily as ctx

# Step 1: Read Data from Excel
# Replace 'AirQualityData.xlsx' with the actual file path
excel_file_path = 'AirQualityData.xlsx'
pm25_data = pd.read_excel(excel_file_path)

# Display the first few rows of the DataFrame to verify the data
print(pm25_data.head())

# Step 2: Filter Data for India
# Assuming your DataFrame has columns 'Lat', 'Long', and 'PM25'
# Use latitude and longitude bounds for India
india_data = pm25_data[(pm25_data['Lat'] >= 8.0) & (pm25_data['Lat'] <= 37.0) &
                       (pm25_data['Long'] >= 68.0) & (pm25_data['Long'] <= 97.0)]

# Step 3: Interpolation and Image Creation
coordinates = india_data[['Lat', 'Long']].values
pm25_values = india_data['PM25'].values

# Define the grid of points for prediction
latitudes = np.linspace(8.0, 37.0, 500)  # Adjust the number of points based on your preference
longitudes = np.linspace(68.0, 97.0, 500)  # Adjust the number of points based on your preference
grid_latitudes, grid_longitudes = np.meshgrid(latitudes, longitudes)
grid_points = np.column_stack((grid_latitudes.flatten(), grid_longitudes.flatten()))

# Perform IDW interpolation using griddata from scipy
predicted_pm25 = griddata(coordinates, pm25_values, grid_points, method='cubic')

# Reshape the predicted values to create a 2D array
pm25_image = predicted_pm25.reshape(len(latitudes), len(longitudes))

# Create a GeoDataFrame for the basemap
gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(india_data['Long'], india_data['Lat']))

# Plot the basemap using contextily
ax = gdf.plot(markersize=10, color='red', alpha=0.5, figsize=(10, 8))
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Overlay the PM2.5 concentration map on the India basemap
plt.imshow(pm25_image, cmap='viridis', extent=[68.0, 97.0, 8.0, 37.0], origin='lower', vmin=0, vmax=500, alpha=0.5)
plt.colorbar(label='PM2.5 Concentration')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('PM2.5 Concentration Map in India (0-500) Overlay')
plt.show()
