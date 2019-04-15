# use selenium to simulate web browser (need to download selenium or create a docker image)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import requests

from pandas import DataFrame

from datetime import datetime
CURRENT_YEAR = datetime.now().year

def load_candidates(path):
	'''
	Takes path to csv and returns a Pandas DataFrame with all the information
	'''
	csv = path

	return DataFrame(csv)

def login(driver, username, password):
	'''
	Logs into website

	Notes:
		Make sure to include Firefox/Chrome driver within you PATH variable
	'''

	u = driver.find_element_by_name('UserID')
	u.clear()
	u.send_keys(username)

	pw = driver.find_element_by_name('PassPhrase')
	pw.clear()
	pw.send_keys(password)

	try:
		driver.find_element_by_name("btnAction").click()
	except Exception as e:
		print(e)


def goto_election_page(driver):
	'''
	Enters the election page to choose between
	Args:
	Returns:c
	Notes:
		Searches through both fall and spring semester election links and selects current semester
		links returns 3 elements 0: fall, 1: spring, 2: officer elections
	'''

	links = driver.find_elements_by_partial_link_text('Election')
	links[1].click() # temp for now

''' Need to replace links[1].click() with this more general statement
	for link in links:
		if CURRENT_YEAR in link:
			link.click()
'''


def check_boxes(driver, classification):
	'''
	Goes through all pages and checks all boxes
	'''
	if classification == 'Junior':
		driver.find_element_by_xpath("//input[@value='Continue to Juniors']").click()
	elif classification == 'Senior':
		driver.find_element_by_xpath("//input[@value='Continue to Seniors']").click()
	else:
		return

	while True:
		for i in range(20):
			try:
				s = Select(driver.find_element_by_name("Rejected" + str(i + 1)))
				s.select_by_value('A2')
			except Exception:
				continue

		try:
			driver.find_elements_by_name('btnAction')[0].click()
			# driver.find_element_by_xpath("//input[@value='Continue']")
		except Exception:
			break
		
	driver.find_elements_by_name('btnAction')[1].click()
	# driver.find_element_by_xpath("//input[@name='btnAction' and @value='Back']")



if __name__ == '__main__':
	driver = webdriver.Chrome('../lib/mac/chromedriver')
	driver.get('https://www.tbp.org/TBPelig/scripts/Login.cfm?Param=482')

	username = input('Enter Username :').strip()
	password = input('Enter Password : ').strip()

	login(driver=driver, username=username, password=password)

	driver.switch_to.frame(driver.find_element_by_name('RightFrame'))
	goto_election_page(driver=driver)
	check_boxes(driver, 'Junior')
	check_boxes(driver, 'Senior')

	# driver.close()

