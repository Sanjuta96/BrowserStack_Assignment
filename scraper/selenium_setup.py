from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless")
    opts.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=opts)
