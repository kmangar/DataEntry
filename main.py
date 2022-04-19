import pprint

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

form_link = "https://forms.gle/82EErXMpxZj81u3Z6"
zillow_link = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

response = requests.get(zillow_link, headers=header)
zillow_sf_rent = response.text

soup = BeautifulSoup(zillow_sf_rent, "html.parser")

# print(soup.title)

properties = soup.findAll(name="div", class_="list-card-info")


# print(soup)
# pprint(zillow_sf_rent)
list_address = [addi.getText() for addi in soup.findAll(name="address", class_="list-card-addr")]
list_link = [link.getText("href") for link in soup.findAll(name="a", class_="list-card-link-top-margin")]

list_price = [price.getText() for price in soup.findAll(name="div", class_="list-card-price")]

print(list_address)
print(list_link)
print(list_price)

#
# driver = webdriver.Chrome("")
#
# driver.get()
#
# driver.find_element(By)
