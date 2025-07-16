from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
from scraper.config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY


def get_browserstack_driver():
    options = Options()

    bstack_options = {
        "os": "Windows",
        "osVersion": "10",
        "local": "false",
        "seleniumVersion": "4.0.0",
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY,
        "sessionName": "El Pais Test",
        "buildName": "Build 1",
    }
    options.set_capability("bstack:options", bstack_options)

    options.browser_name = "chrome"
    options.browser_version = "latest"

    driver = webdriver.Remote(
        command_executor='https://hub.browserstack.com/wd/hub',
        options=options
    )
    return driver


def handle_cookie_popup(driver):
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="didomi-notice-agree-button"]'))
        )
        accept_button.click()
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "didomi-notice"))
        )
        print("Cookie popup accepted and closed.")
    except TimeoutException:
        print("No cookie popup appeared or it was already handled.")


def click_opinion_link(driver):
    opinion_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/opinion')]")
    print(f"Found {len(opinion_links)} opinion links")

    for link in opinion_links:
        if link.is_displayed() and link.is_enabled():
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
                time.sleep(0.5)  # small wait after scrolling

                # Try normal click first
                try:
                    link.click()
                    print("✅ Clicked on visible Opinion link (normal click).")
                    return True
                except ElementClickInterceptedException as e:
                    print(f"⚠️ Normal click intercepted: {e}. Trying JS click...")

                    # Fall back to JS click
                    driver.execute_script("arguments[0].click();", link)
                    print("✅ Clicked on visible Opinion link (JS click).")
                    return True
            except Exception as e:
                print(f"❌ Click failed: {e}. Trying next link...")
                continue

    print("❌ No clickable Opinion link found.")
    return False


def test_el_pais_on_browserstack():
    driver = get_browserstack_driver()
    driver.get("https://elpais.com")

    time.sleep(3)  # Wait for popup to appear

    handle_cookie_popup(driver)

    if not click_opinion_link(driver):
        driver.quit()
        raise Exception("Could not click any Opinion link")

    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    test_el_pais_on_browserstack()
