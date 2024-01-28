const base_url = "https://api.waqi.info";
const token = "6adbc6ff13fe01a446ff9fb49c7d993d69d71fe3"; // Replace with your actual API token
const fs = require('fs');

async function fetchDataForCities() {
  try {
    const data = await fs.promises.readFile('stations.txt', 'utf8');
    const cityData = data.split('\n');
    const cleanedCityData = cityData.filter(Boolean);

    for (const city of cleanedCityData) {
      const response = await fetch(`${base_url}/feed/${city.toLowerCase()}/?token=${token}`);

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log(data);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

fetchDataForCities();
