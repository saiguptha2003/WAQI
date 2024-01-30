import numpy as np
from scipy.spatial.distance import cdist
from scipy.interpolate import griddata

def idw_interpolation(data, target_points, power=2):
    coordinates = data[['Lat', 'Long']].values
    values = data[column_name].values

    distances = cdist(target_points, coordinates)
    weights = 1 / (distances + 1e-10)**power
    weights /= np.sum(weights, axis=1, keepdims=True)

    interpolated_values = np.sum(weights * values, axis=1)
    return interpolated_values

column_name = 'PM25'
target_latitudes = np.linspace(8.0, 37.0, 500)
target_longitudes = np.linspace(68.0, 97.0, 500)
target_points = np.column_stack((target_latitudes, target_longitudes))

interpolated_values = idw_interpolation(pm25_data, target_points)
image = interpolated_values.reshape(len(target_latitudes), len(target_longitudes))

plt.imshow(image, cmap='viridis', extent=[68.0, 97.0, 8.0, 37.0], origin='lower', vmin=0, vmax=350)
plt.colorbar(label=f'{column_name} Concentration')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title(f'{column_name} Concentration Map (IDW)')
plt.show()
