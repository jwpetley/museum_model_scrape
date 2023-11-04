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

    thumbs = soup.find_all("span", class_= "b-text-wrapper")

    # Get the model links
    collections = []
    for item in thumbs:
        collections.append(item.find("span", class_= "title h3").get_text())


    return collections

def get_pieces(collection):
    collection = collection.lower()
    url = f"https://3d.si.edu/collections/{collection}"
    page = requests.get(url)

    # Parse the page
    soup = BeautifulSoup(page.text, 'html.parser')


    thumbs = soup.find_all("div", class_= "teaser teaser-long")
    links = []
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

def get_model(piece_link):
    driver = webdriver.Chrome(options = options)
    driver.get(piece_link)
    text = "heading-tab-download"
    download_button = driver.find_element(By.XPATH, f"//button[@id='{text}']")
    download_button.click()


    try:
        file_type = "\"150k-4096-obj_std.zip\""

        usdz_file = driver.find_element(By.XPATH, f"//a[contains(., {file_type})]")
        usdz_file.click()

        seconds = download_wait(download_dir, 300)

        print("Download took {} seconds.".format(seconds))
    except: 
        "Cannot download .usdz for this model."

    driver.quit()

def push_to_cloud(folder):
    '''Function takes directory and uploads zip files to google cloud bucket'''
    import subprocess

    subprocess.run(["gcloud", "storage", "cp", folder+"/*.zip", "gs://init-museum-models/"])

    return None







if __name__ == "__main__":

    download_dir = "/home/qjfn45/Documents/museum_model_scrape/models"

    options = Options()
    options.add_experimental_option('prefs',  {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "profile.managed_default_content_settings.images": 2,
    }   
    )

    url = "https://3d.si.edu/collections"

    collections = get_collections(url)


    pieces = get_pieces(collections[0])


    #for piece in pieces:
    #    get_model(piece)

    push_to_cloud(download_dir)




