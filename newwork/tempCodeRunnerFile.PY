import selenium as se
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from PIL import Image
# text recognition
import time
import cv2
import pytesseract

driver = webdriver.Edge()
driver.get("https://airquality.cpcb.gov.in/AQI_India/")

x = 536
y = 100
width = 400
height = 100
print(x, y, x + width, y + height)

driver.save_screenshot("screenshot.png")
im = Image.open("screenshot.png")
im = im.crop((int(x), int(y), int(x + width), int(y + height)))
im.save("captcha.png")
import easyocr
reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
result = reader.readtext('captcha.png')