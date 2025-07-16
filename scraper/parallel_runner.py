from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scraper.config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY

def get_browserstack_driver():
    bstack_options = {
        "os": "Windows",
        "osVersion": "10",
        "local": "false",
        "seleniumVersion": "4.0.0",
        "sessionName": "El Pais Test",
        "buildName": "Build 1"
    }

    options = Options()
    options.set_capability("bstack:options", bstack_options)
    options.browser_name = "chrome"
    options.browser_version = "latest"

    # Embed credentials in URL (works fine)
    executor_url = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub.browserstack.com/wd/hub"

    driver = webdriver.Remote(
        command_executor=executor_url,
        options=options
    )
    return driver


def main():
    driver = get_browserstack_driver()
    driver.get("https://elpais.com")
    print("Page title is:", driver.title)
    driver.quit()

if __name__ == "__main__":
    main()
