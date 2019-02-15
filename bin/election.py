# use selenium to simulate web browser (need to download selenium or create a docker image)
from selenium import webdriver
import requests

with requests.Session() as s:
	driver = webdriver.Chrome()
	driver.get("https://example.com")
	button = driver.find_element_by_id('buttonID')
	button.click()

