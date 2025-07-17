# runners/parallel_runner.py

import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scraper.config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY
from scraper.translator import translate_titles

BROWSERS = [
    {"os": "Windows", "browser": "Chrome"},
    {"os": "OS X", "browser": "Safari"},
    {"os": "Windows", "browser": "Edge"},
    {"deviceName": "Samsung Galaxy S21", "realMobile": "true", "browser": "Chrome"},
    {"deviceName": "iPhone 14", "realMobile": "true", "browser": "Safari"},
]

def get_driver(config):
    bstack_options = {
        "os": config.get("os"),
        "browserName": config.get("browser"),
        "browserVersion": "latest",
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY,
        "sessionName": f"{config.get('deviceName', config['browser'])} Test",
        "buildName": "Parallel Test Build",
    }

    if "deviceName" in config:
        bstack_options["deviceName"] = config["deviceName"]
        bstack_options["realMobile"] = config.get("realMobile", "true")
        bstack_options.pop("os", None)  # mobile configs don't use "os"

    options = webdriver.ChromeOptions()
    options.set_capability("bstack:options", bstack_options)

    return webdriver.Remote(
        command_executor='https://hub.browserstack.com/wd/hub',
        options=options
    )

def scrape_and_translate(config):
    try:
        driver = get_driver(config)
        driver.get("https://elpais.com")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        try:
            accept = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
            )
            accept.click()
        except:
            pass  # Cookie banner may not always appear

        opinion_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/opinion')]")
        for link in opinion_links:
            if link.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", link)
                break

        time.sleep(3)
        article_elems = driver.find_elements(By.CSS_SELECTOR, "article a")[:5]
        articles = [{"title_es": elem.text.strip()} for elem in article_elems if elem.text.strip()]
        translated = translate_titles(articles)

        platform = f"{config.get('deviceName', config['browser'])} on {config.get('os', 'mobile')}"
        print(f"\n📲 {platform} — Translated titles:")
        for article in translated:
            print(f"- {article['title_en']}")

        driver.quit()

    except Exception as e:
        platform = f"{config.get('deviceName', config.get('browser'))} on {config.get('os', 'mobile')}"
        print(f"❌ Error in {platform}: {e}")

def main():
    threads = []
    for config in BROWSERS:
        t = threading.Thread(target=scrape_and_translate, args=(config,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
