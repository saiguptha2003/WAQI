import requests
import openpyxl

base_url = "https://api.waqi.info"
token = "6adbc6ff13fe01a446ff9fb49c7d993d69d71fe3"  # Replace with your actual API token

response = requests.get(f"{base_url}/v2/map/bounds?token={token}&latlng=8.0667,68.1167,37.1,97.4167&networks=all")

if response.ok:
    data = response.json()

    if data.get("status") == "ok" and data.get("data") and len(data["data"]) > 0:
        # Extract relevant information from the data
        stations_info = [
            {
                "uid": station["uid"],
                "name": station["station"]["name"],
                "latitude": station["lat"],
                "longitude": station["lon"],
                "aqi": station["aqi"],
            }
            for station in data["data"]
        ]

        # Create a new Excel workbook and add a worksheet
        workbook = openpyxl.Workbook()
        worksheet = workbook.active

        # Write titles to the worksheet
        titles = ["UID", "Name", "Latitude", "Longitude", "AQI"]
        worksheet.append(titles)

        # Write data to the worksheet
        for station_info in stations_info:
            row_data = [station_info.get(key, '') for key in titles]
            worksheet.append(row_data)

        # Save the workbook to a file
        workbook.save("stations.xlsx")
        print("Excel file 'stations.xlsx' created successfully.")
    else:
        print("Invalid data structure or no stations found.")
else:
    print(f"HTTP error! Status: {response.status_code}")
