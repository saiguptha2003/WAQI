const base_url = "https://api.waqi.info";
const token = "6adbc6ff13fe01a446ff9fb49c7d993d69d71fe3";
const fs = require('fs');
const ExcelJS = require('exceljs');

async function fetchDataForCities() {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet('AirQualityData');
  const unknownWorksheet = workbook.addWorksheet('UnknownStations');

  // Add headers to the worksheets
  worksheet.addRow(['Idx', 'City', 'AQI', 'Lat', 'Long', 'CO', 'H', 'NO2', 'O3', 'P', 'PM10', 'PM25', 'SO2', 'Time']);
  unknownWorksheet.addRow(['City']);

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
        console.log(`Station is unknown for city: ${city}`);
        unknownWorksheet.addRow([city]);
        continue; // Skip to the next iteration
      }

      const { idx, city: { name }, aqi, city: { geo: [lat,long] }, iaqi, time: { s } } = responseData.data;

      // Initialize variables to handle undefined properties
      let coValue = hValue = no2Value = o3Value = pValue = pm10Value = pm25Value = so2Value = '';

      // Check if properties are defined before accessing
      if (iaqi && iaqi.co && iaqi.co.v) coValue = iaqi.co.v;
      if (iaqi && iaqi.h && iaqi.h.v) hValue = iaqi.h.v;
      if (iaqi && iaqi.no2 && iaqi.no2.v) no2Value = iaqi.no2.v;
      if (iaqi && iaqi.o3 && iaqi.o3.v) o3Value = iaqi.o3.v;
      if (iaqi && iaqi.p && iaqi.p.v) pValue = iaqi.p.v;
      if (iaqi && iaqi.pm10 && iaqi.pm10.v) pm10Value = iaqi.pm10.v;
      if (iaqi && iaqi.pm25 && iaqi.pm25.v) pm25Value = iaqi.pm25.v;
      if (iaqi && iaqi.so2 && iaqi.so2.v) so2Value = iaqi.so2.v;

      // Check if pm25Value is empty before adding the data
      // if (!pm25Value || !pm10Value){
      //   console.log(`Skipping city ${name} due to missing PM25 value.`);
      //   continue;
      // }

      // Format numbers with more precision (e.g., 6 decimal places)
      const formattedLat = parseFloat(lat).toFixed(6);
      const formattedLong = parseFloat(long).toFixed(6);

      // Add data to the worksheet
      worksheet.addRow([idx, name, aqi, formattedLat, formattedLong, coValue, hValue, no2Value, o3Value, pValue, pm10Value, pm25Value, so2Value, s]);
    }

    // Save the workbook to separate files
    await Promise.all([
      workbook.xlsx.writeFile('AirQualityData.xlsx'),
      workbook.xlsx.writeFile('UnknownStations.xlsx')
    ]);

    console.log('Excel files created successfully.');
  } catch (error) {
    console.error('Error:', error);
  }
}
fetchDataForCities();