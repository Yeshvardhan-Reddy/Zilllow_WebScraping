from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from time import sleep

GOOGLE_FORM = ''  # create a Google form and insert the link here eg: https://forms.gle/nF3fvhnEK18tmjbF9
ZILLOW_URL = ''  # type your zillow website url here
# Go to https://myhttpheader.com/ and pass in the following headers
HEADERS = {
    "User-Agent": "",
    "Accept-Language": "",
    "Accept-Encoding": "",
}
response = requests.get(url=ZILLOW_URL, headers=HEADERS)
webpage = response.content
soup = BeautifulSoup(webpage, 'lxml')
# print(soup)
table = soup.find("div", {"id": "search-page-list-container"}).find_next('ul')

all_elements = table.findAll('li')
addresses = [element.find_next('a').text for element in all_elements]
links = [element.find_next('a')['href'] for element in all_elements]
for i in range(len(links)):
    if "https://www.zillow.com" not in links[i]:
        links[i] = "https://www.zillow.com" + links[i]

price_element = table.find_all('span', {"data-test": "property-card-price"})
prices = [price.text for price in price_element]
for i in range(len(prices)):
    print(f"{addresses[i]}||{prices[i]}||{links[i]}")


options = Options()
options.add_experimental_option("detach", True)
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(GOOGLE_FORM)
sleep(4)

for i in range(len(prices)):
    address = driver.find_element(by=By.XPATH,
                                  value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]'
                                        '/div/div[1]/input')
    price = driver.find_element(by=By.XPATH,
                                value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/'
                                      'div/div[1]/input')
    visit_link = driver.find_element(by=By.XPATH,
                                     value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/'
                                           'div[1]/div/div[1]/input')
    submit = driver.find_element(by=By.XPATH,
                                 value='/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    address.send_keys(addresses[i])
    price.send_keys(prices[i])
    visit_link.send_keys(links[i])
    sleep(2)
    submit.click()
    sleep(2)
    next_response = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    next_response.click()

driver.close()
