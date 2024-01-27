const base_url = "https://api.waqi.info";
const token = "6adbc6ff13fe01a446ff9fb49c7d993d69d71fe3"; // Replace with your actual API token
const XLSX = require('xlsx');

fetch(`${base_url}/v2/map/bounds?token=${token}&latlng=8.0667,68.1167,37.1,97.4167&networks=all`)
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    if (data && data.status === 'ok' && data.data && data.data.length > 0) {
      // Extract relevant information from the data
      const stationsInfo = data.data.map(station => ({
        uid: station.uid,
        name: station.station.name,
        latitude: station.lat,
        longitude: station.lon,
        aqi: station.aqi,
      }));

      if (stationsInfo.length > 0) {
        // Get the titles dynamically from the first station
        const titles = Object.keys(stationsInfo[0]);

        // Create a worksheet with titles
        const ws = XLSX.utils.json_to_sheet([titles, ...stationsInfo], { header: titles });

        // Create a workbook with the worksheet
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, 'Stations');

        // Save the workbook to a file
        XLSX.writeFile(wb, 'stations.xlsx');
      } else {
        console.error('No station data found.');
      }
    } else {
      console.error('Invalid data structure or no stations found.');
    }
  })
  .catch(error => {
    console.error('Fetch error:', error);
  });
