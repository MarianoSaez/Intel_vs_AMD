from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

link = 'https://openbenchmarking.org/tests'

# Abrir el navegador y cargar pagina
driver = webdriver.Firefox()
driver.get(link)
webElement_list = driver.find_elements_by_tag_name('a')
link_list = list()

for i in webElement_list:
    link_list.append(i.get_attribute('href'))

print(f'{len(link_list)} will be opened')

for i in link_list:
    driver.implicitly_wait(5)
    driver.get(f'{i}')
    time.sleep(5)
driver.close()
