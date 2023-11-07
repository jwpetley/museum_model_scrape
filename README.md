# Digital Pantheon

Code to scrape 3d models from museums and upload to google cloud storage. 

This repository was made for Durhack 2023 and involves beautiful soup webscraping, google cloud storage and a bit of python.

A website was created using gh-pages and jekyll and can be viewed at [https://digitalpantheon.study/about](https://digitalpantheon.study/about). 

### How to run

1. Clone the repository
2. Install the requirements using `pip install -r requirements.txt`
3. Run the script using `python3 smithsonian_scrape.py` for Smithsonian museum and `python3 nhm_scrape.py` for the Natural History Museum, UK.

Note that you will need appropriate google cloud authorisation setup as well as the correct chromedriver in order for these to run.
