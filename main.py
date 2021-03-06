import pprint
import time

from bs4 import BeautifulSoup
import lxml
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

# TODO: USE BS4 to scrape the data

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

form_link = "your google form"
zillow_link = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

response = requests.get(zillow_link, headers=header)
data = response.text

soup = BeautifulSoup(data, "html.parser")

# print(soup.title)

properties = soup.findAll(name="div", class_="list-card-info")

# TODO:: create a list with all the links and if it's missing parts in the link fill it in
all_link_elements = soup.select(".list-card-top a")
all_links = []
for link in all_link_elements:
    href = link["href"]
    # print(href)
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

# TODO: store all the address in a list. clean the address formatting
list_address = [address.get_text().split(" | ")[-1] for address in
                soup.findAll(name="address", class_="list-card-addr")]

# TODO: store all the rental price in a list and clean formatting
list_price = [price.getText().split("+")[0] for price in soup.findAll(name="div", class_="list-card-price")]

# output for visual testing purpose
print(f"{list_address}\nlen: {len(list_address)}")
print(f"{all_links}\nlen: {len(all_links)}")
print(f"{list_price}\nlen: {len(list_price)}")

# TODO: USING Selenium fill in the google form

# Assign driver with the chrome path
driver = webdriver.Chrome("chromedriver.exe")

# Use the driver to go to the form
driver.get(form_link)
# sleep for 5sec for the form to load
time.sleep(3)

for x in range(len(list_address)):
    # after the page loads find the property address field and enter the data
    property_field = driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    property_field.send_keys(list_address[x])

    # Enter price next
    price_field = driver.find_element(By.XPATH,
                                      '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_field.send_keys(list_price[x])

    # Enter property link next
    property_link = driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    property_link.send_keys(all_links[x])

    # submit the response
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit.click()

    # sleep for 5 sec and click onm sar(submit another response)
    time.sleep(2)
    # '/html/body/div[1]/div[2]/div[1]/div/div[4]/a'
    sar = driver.find_element(By.XPATH,
                        '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    sar.click()

# print(f"Finished Data Entry in google form check by going to {form_link}")
driver.quit()





















































