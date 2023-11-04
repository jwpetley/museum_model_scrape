from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_file(url):
    driver = webdriver.Chrome()
    driver.get(url)
    download_button = driver.find_element(By.ID, 'Download Free 3D Model')
    download_button.click()
    driver.quit()

# Get the page
url = 'https://sketchfab.com/artfletch/collections/british-museum-89e61180ae9e47789fb02b3109d33f98'
page = requests.get(url)

# Parse the page
soup = BeautifulSoup(page.text, 'html.parser')

items = soup.find_all("div", class_= "c-grid__item")
#print(soup.prettify())
print(items)
# Get the model links
links = []
for item in items:
    links.append(item.find("meta", itemprop = "url", content = True).get("content"))

# Download the models
for link in links:
    get_file(link)
    