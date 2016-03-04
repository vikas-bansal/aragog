from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get('http://web.mit.edu/')
inputElement = driver.find_element_by_id("searchBox")
inputElement.send_keys('faculty')
inputElement.send_keys(Keys.ENTER)
