from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def get_file(url):
    driver = webdriver.Chrome()
    driver.get(url)
    cookies = driver.find_element(By.ID, "onetrust-reject-all-handler")
    cookies.click()
    title_text = "Download Free 3D Model"
    download_button = driver.find_element(By.XPATH, f"//button[@title='{title_text}']")
    download_button.click()
    user = 'email'
    username = driver.find_element(By.XPATH, f"//input[@type='{user}']")
    
    if username:
        email = "heather.sm555@gmail.com"
        pw = "Password123!"
        key = 'password'
        password = driver.find_element(By.XPATH, f"//input[@type='{key}']")
        ActionChains(driver)\
            .send_keys_to_element(username, email)\
            .perform()
        ActionChains(driver)\
            .send_keys_to_element(password, pw)\
            .perform()

    obj = "jv075PB9"
    objelement = driver.find_element(By.XPATH, f"//div[@class='{obj}']")
    objbutton = objelement.find_element(By.CLASS_NAME, "button btn-primary btn-small button-source")
    objbutton.click()
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
    