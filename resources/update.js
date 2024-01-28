const base_url = "https://api.waqi.info";
const token = "6adbc6ff13fe01a446ff9fb49c7d993d69d71fe3";
const fs = require('fs');
const fetch = require('node-fetch');
const ExcelJS = require('exceljs');

async function fetchDataForCities() {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet('AirQualityData');

  // Add headers to the worksheet
  worksheet.addRow(['Idx', 'City', 'AQI', 'Lat', 'Long', 'CO', 'H', 'NO2', 'O3', 'P', 'PM10', 'PM25', 'SO2', 'Time']);

  try {
    const data = await fs.promises.readFile('stations.txt', 'utf8');
    const cityData = data.split('\n');
    const cleanedCityData = cityData.filter(Boolean);

    for (const city of cleanedCityData) {
      const response = await fetch(`${base_url}/feed/${city.toLowerCase()}/?token=${token}`);

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const responseData = await response.json();

      // Check if the station information is available
      if (responseData.status === 'error' && responseData.data === 'Unknown station') {
        continue; // Skip to the next iteration
      }
      console.log(console.log(responseData.data.city.name,"asdfasdfasdf"))

      const { idx, city: { name }, aqi, city: { geo: [lat, long] },  iaqi: { co, h, no2, o3, p, pm10, pm25, so2 }, time: { s } } = responseData.data;
      // Format numbers with more precision (e.g., 6 decimal places)
      const formattedLat = parseFloat(lat).toFixed(6);
      const formattedLong = parseFloat(long).toFixed(6);
      console.log(idx, name, aqi, lat, long, co.v, h.v, no2.v, o3.v, p.v, pm10.v, pm25.v, so2.v, s)
   
      // Add data to the worksheet


      // Add data to the worksheet
      worksheet.addRow([idx, name, aqi, lat, long, co.v, h.v, no2.v, o3.v, p.v, pm10.v, pm25.v, so2.v, s]);
    }
    await workbook.xlsx.writeFile('AirQualityData.xlsx');
    console.log('Excel file created successfully.');
  } catch (error) {
    console.error('Error:', error);
  }
}

fetchDataForCities();
