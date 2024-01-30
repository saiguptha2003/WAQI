from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def get_air_quality(city_name):
    # Create a WebDriver (EdgeDriver)
    driver = webdriver.Edge()

    # Load the website
    driver.get('https://airquality.cpcb.gov.in/AQI_India/')  # Replace with the actual URL

    # Select the city from the dropdown
    dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'stations'))
    )
    dropdown = Select(dropdown)
    dropdown.select_by_visible_text(city_name)

    # Wait for the page to update (you may need to use WebDriverWait)
    # Extract the updated HTML
    updated_html = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'graph-container'))
    ).get_attribute('outerHTML')

    # Close the WebDriver
    driver.quit()

    # Parse the updated HTML using BeautifulSoup
    soup = BeautifulSoup(updated_html, 'html.parser')

    # Extract and print air quality information
    attribute_name = soup.find('td', class_='element-name').text
    average_value = soup.find('td', class_='avg-value').text

    print("City:", city_name)
    print("Attribute Name:", attribute_name)
    print("Average Value:", average_value)

# Example: Get air quality for a specific city (replace 'Delhi' with the desired city)
get_air_quality('Delhi')
