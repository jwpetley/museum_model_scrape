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

    thumbs = soup.find_all("div", class_= "edan-embed-content has-media teaser teaser-long entity")

    # Get the model links
    collections = {}
    for item in thumbs:
        collection_link = item.find("a", class_ = "inner").get("href")
        collections[item.find("span", class_= "title h3").get_text()] = collection_link 


    return collections

def get_pieces(collection):
    base_url = "https://3d.si.edu/"
    url = f"https://3d.si.edu/{collections[collection]}"
    print(url)
    page = requests.get(url)


    # Parse the page
    soup = BeautifulSoup(page.text, 'html.parser')

    links = []
    while soup.find("li", class_ = "pager-next") is not None:
        next_page = soup.find("li", class_ = "pager-next").find("a").get("href")
        page = requests.get(base_url + next_page)
        soup = BeautifulSoup(page.text, 'html.parser')


        thumbs = soup.find_all("div", class_= "teaser teaser-long")
    
        for thumb in thumbs:
            link_elements = thumb.find('a')
            link = link_elements.get('href')
            links.append("https://3d.si.edu"+link)

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
    }   
    )

    WINDOW_SIZE = "1920,1080"

    options.add_argument("--headless")
    options.add_argument("--window-size=%s" % WINDOW_SIZE)
    

    driver = webdriver.Chrome(options = options)
    driver.get(piece_link)
    text = "heading-tab-download"
    download_button = driver.find_element(By.XPATH, f"//button[@id='{text}']")
    download_button.click()
    

    try:
        try:
            file_type = "\"Low Resolution 3D Mesh, OBJ\""
            usdz_file = driver.find_element(By.XPATH, 
                                            f"//a[contains(., {file_type})]")
        
        except:
            try:
                file_type = "\"Low Resolution 3D mesh, obj\""
                usdz_file = driver.find_element(By.XPATH, 
                                            f"//a[contains(., {file_type})]")
            except:
                file_type = "\"Low resolution 3D mesh, obj\""
                usdz_file = driver.find_element(By.XPATH, 
                                            f"//a[contains(., {file_type})]")


        file_name = usdz_file.get_attribute("href").split("/")[-1]

       
        if file_name in os.listdir(download_dir):
            print("File already exists.")
            return None
        
        driver.execute_script("arguments[0].scrollIntoView();", usdz_file)
        usdz_file.click()

        seconds = download_wait(download_dir, 300)

        print("Download took {} seconds.".format(seconds))
    except: 
        pass

    driver.quit()

def push_to_cloud(folder):
    '''Function takes directory and uploads zip files to google cloud bucket'''
    import subprocess

    subprocess.run(["gcloud", "storage", "cp", folder+"/*.zip", "gs://init-museum-models/"])

    return None







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


    url = "https://3d.si.edu/collections"

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
            get_model(piece, download_dir)
            print("Downloaded model {} from collection {}.".format(piece, collection))

    #push_to_cloud(download_dir)




