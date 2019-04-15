from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests.help

from datetime import datetime
CURRENT_YEAR = datetime.now().year

driver = webdriver.Chrome('../lib/mac/chromedriver')
driver.get('https://www.google.com')

links = driver.find_elements_by_partial_link_text('Gmail')
print(len(links))

# driver.close()