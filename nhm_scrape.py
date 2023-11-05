from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import os

def get_collections(url):
    page = requests.get(url)

    # Parse the page
    soup = BeautifulSoup(page.text, 'html.parser')


    thumbs = soup.find_all("div", class_= "c-grid__item item")
    
    # Get the model links
    collections = {}
    for item in thumbs:
        collection_link = item.find("a", class_ = "label").get("href")
        collections[item.find("a", class_= "label").get("title")] = collection_link 

    return collections

def get_pieces(collection):
    #base_url = "https://sketchfab.com/NHM_Imaging/collections"
    #url = f"https://sketchfab.com/NHM_Imaging/collections{collections[collection]}"
    #print(url)
    page = requests.get(collections[collection])

    # Parse the page
    soup = BeautifulSoup(page.text, 'html.parser')

    links = []
    #while soup.find("li", class_ = "pager-next") is not None:
    #    next_page = soup.find("li", class_ = "pager-next").find("a").get("href")
    #    page = requests.get(base_url + next_page)
    #    soup = BeautifulSoup(page.text, 'html.parser')


    thumbs = soup.find_all("div", class_= "c-grid__item item")
    
    for thumb in thumbs:
        link_elements = thumb.find('a', class_= "help card-model__feature --downloads")
        link = link_elements.get('href')
        links.append(link)

    return links

def download_wait(directory, timeout, nfiles=None):
    """
    Wait for downloads to finish with a specified timeout.

    Args
    ----
    directory : str
        The path to the folder where the files will be downloaded.
    timeout : int
        How many seconds to wait until timing out.
    nfiles : int, defaults to None
        If provided, also wait for the expected number of files.

    """
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        sleep(1)
        dl_wait = False
        files = os.listdir(directory)
        if nfiles and len(files) != nfiles:
            dl_wait = True

        for fname in files:
            if fname.endswith('.crdownload'):
                dl_wait = True

        seconds += 1
    return seconds

def get_model(piece_link, download_dir):

    options = Options()
    options.add_experimental_option('prefs',  {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "profile.managed_default_content_settings.images": 2,
    "profile.default_content_settings.popups": 0,
    # Cookies
    "profile.default_content_setting_values.cookies": 1,
    }   
    )

    options.add_argument(r"--user-data-dir=/home/qjfn45/.config/google-chrome/Default") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
    options.add_argument(r'--profile-directory=Default') #e.g. Profile 3

    WINDOW_SIZE = "1920,1080"

    options.add_argument("--headless")
    options.add_argument("--window-size=%s" % WINDOW_SIZE)
    

    driver = webdriver.Chrome(options = options)
    driver.get(piece_link)

    #email = driver.find_element(By.XPATH, "//input[@name='email']")
    #password = driver.find_element(By.XPATH, "//input[@type='password']")

    #email.send_keys("heather.sm555@gmail.com")
    #password.send_keys("Password123!")

    #button = driver.find_element(By.XPATH, "//button[@data-selenium='submit-button']")
    #button.click()
    




    try:

        text = "button btn-primary btn-small button-source"
        objtext = 'jv075PB9'
        obj = driver.find_element(By.XPATH, f"//div[@class='{objtext}']")
        download_button = obj.find_element(By.XPATH, f"//button[@class='{text}']")
        download_button.click()

        seconds = download_wait(download_dir, 300)
        print("Download took {} seconds.".format(seconds))
    except:
        pass

    
    #except: 
    #    pass

    driver.quit()

if __name__ == "__main__":

    download_dir_base = "/home/qjfn45/Documents/museum_model_scrape/models"

    options = Options()
    options.add_experimental_option('prefs',  {
    "download.default_directory": download_dir_base,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "profile.managed_default_content_settings.images": 2,
    
    }   
    )

    url =  "https://sketchfab.com/NHM_Imaging/collections" 

    collections = get_collections(url)
    print(collections)

    for collection in collections:
        pieces = get_pieces(collection)
        print(collection, pieces)
        download_dir = download_dir_base + "/" + collection
        try:
            os.mkdir(download_dir)
        except:
            print("Directory already exists.")


        for piece in pieces:
            print(piece)
            get_model(piece, download_dir)
            print("Downloaded model {} from collection {}.".format(piece, collection))

    #push_to_cloud(download_dir)
