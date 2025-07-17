# el_pais_scraper/scraper/browserstack_runner.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

from scraper.config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY
from scraper.article_scraper import scrape_opinion_articles
from scraper.translator import translate_titles


def get_browserstack_driver():
    """Initialize and return a BrowserStack remote WebDriver."""
    options = webdriver.ChromeOptions()
    bstack_opts = {
        "os": "Windows",
        "osVersion": "10",
        "browserName": "Chrome",
        "browserVersion": "latest",
        "sessionName": "ElPais BrowserStack Test",
        "buildName": "BStack Build 1",
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY,
        "seleniumVersion": "4.20.0"
    }
    options.set_capability('bstack:options', bstack_opts)

    driver = webdriver.Remote(
        command_executor='https://hub.browserstack.com/wd/hub',
        options=options
    )
    return driver


def main():
    driver = get_browserstack_driver()

    try:
        articles = scrape_opinion_articles(driver, limit=5)
        translated = translate_titles(articles)

        # Take a screenshot and save it
        screenshot_path = os.path.join("screenshots", "browserstack_result.png")
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(screenshot_path)
        print(f"\n📸 Screenshot saved to: {screenshot_path}")

        print("\n📋 Translated Titles:")
        for article in translated:
            print(f"- {article['title_en']}")

    except Exception as e:
        print(f"❌ Error during BrowserStack run: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
