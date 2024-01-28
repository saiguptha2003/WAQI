import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import subprocess

# Replace 'your_script.js' with the actual path to your JavaScript file
javascript_file = 'excel.js'

# Run the JavaScript file using Node.js
result = subprocess.run(['node', javascript_file], capture_output=True, text=True)

# Print the output
print("JavaScript Output:", result.stdout)

# Check for errors
if result.returncode != 0:
    print("Error:", result.stderr)
excel_file_path = 'AirQualityData.xlsx'
pm25_data = pd.read_excel(excel_file_path)

print(pm25_data.head())

coordinates = pm25_data[['Lat', 'Long']].values
pm25_values = pm25_data['PM25'].values

latitudes = np.linspace(8.0, 37.0, 500) 
longitudes = np.linspace(68.0, 97.0, 500) 
grid_latitudes, grid_longitudes = np.meshgrid(latitudes, longitudes)
grid_points = np.column_stack((grid_latitudes.flatten(), grid_longitudes.flatten()))

predicted_pm25 = griddata(coordinates, pm25_values, grid_points, method='cubic')

pm25_image = predicted_pm25.reshape(len(latitudes), len(longitudes))

plt.imshow(pm25_image, cmap='viridis', extent=[68.0, 97.0, 8.0, 37.0], origin='lower', vmin=0, vmax=350)
plt.colorbar(label='PM2.5 Concentration')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('PM2.5 Concentration Map (0-500)')
plt.show()
