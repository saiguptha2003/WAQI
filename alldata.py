import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

def interpolate_and_plot(data, column_name, vmin=0, vmax=350, output_file=None):
    # Check if the specified column contains missing values
    if data[column_name].isnull().any():
        print(f"Removing rows with missing values in '{column_name}'.")
        data = data.dropna(subset=[column_name])

    coordinates = data[['Lat', 'Long']].values
    values = data[column_name].values

    latitudes = np.linspace(8.0, 37.0, 500)
    longitudes = np.linspace(68.0, 97.0, 500)
    grid_latitudes, grid_longitudes = np.meshgrid(latitudes, longitudes)
    grid_points = np.column_stack((grid_latitudes.flatten(), grid_longitudes.flatten()))

    predicted_values = griddata(coordinates, values, grid_points, method='cubic')

    image = predicted_values.reshape(len(latitudes), len(longitudes))

    plt.imshow(image, cmap='viridis', extent=[68.0, 97.0, 8.0, 37.0], origin='lower', vmin=vmin, vmax=vmax)
    plt.colorbar(label=f'{column_name} Concentration')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'{column_name} Concentration Map ({vmin}-{vmax})')
    if output_file:
        plt.savefig(output_file, format='tiff', dpi=300)
    
    plt.show()


javascript_file = 'excel.js'
result = subprocess.run(['node', javascript_file], capture_output=True, text=True)
print("JavaScript Output:", result.stdout)
if result.returncode != 0:
    print("Error:", result.stderr)
excel_file_path = 'AirQualityData.xlsx'
output_directory = 'output_images/'
pm25_data = pd.read_excel(excel_file_path)
interpolate_and_plot(pm25_data, 'PM25', vmin=0, vmax=350, output_file=output_directory + 'PM25_concentration_map.tiff')
interpolate_and_plot(pm25_data, 'AQI', vmin=0, vmax=350, output_file=output_directory + 'PM25_concentration_map.tiff')
interpolate_and_plot(pm25_data, 'PM10', vmin=0, vmax=350, output_file=output_directory + 'PM10_concentration_map.tiff')
interpolate_and_plot(pm25_data, 'CO', vmin=0, vmax=350, output_file=output_directory + 'CO.tiff')
interpolate_and_plot(pm25_data, 'NO2', vmin=0, vmax=350, output_file=output_directory + 'No2.tiff')
interpolate_and_plot(pm25_data, 'H', vmin=0, vmax=350, output_file=output_directory + 'H.tiff')
