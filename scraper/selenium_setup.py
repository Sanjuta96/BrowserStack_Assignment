from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
import time

def get_driver_and_navigate():
    options = webdriver.ChromeOptions()
    # Uncomment to run headless
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("https://elpais.com")

    wait = WebDriverWait(driver, 15)

    # Wait for cookie popup and accept
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

    try:
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".overlay-selector"))
        )
        print("Overlay disappeared.")
    except TimeoutException:
        print("No overlay detected or still present.")

    # Find all Opinion links
    opinion_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/opinion')]")
    print(f"Found {len(opinion_links)} opinion links")

    for i, link in enumerate(opinion_links):
        print(f"Link {i}: text='{link.text}', href='{link.get_attribute('href')}', displayed={link.is_displayed()}, enabled={link.is_enabled()}")

    # Click first visible & enabled Opinion link with robust method
    clicked = False
    for link in opinion_links:
        if link.is_displayed() and link.is_enabled():
            try:
                # Scroll into center view
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
                time.sleep(1)  # small pause after scrolling

                try:
                    link.click()
                    print("✅ Clicked on visible Opinion link (normal click).")
                except ElementClickInterceptedException as e:
                    print(f"⚠️ Normal click intercepted: {e}. Trying ActionChains click...")
                    try:
                        actions = ActionChains(driver)
                        actions.move_to_element(link).click().perform()
                        print("✅ Clicked on visible Opinion link (ActionChains click).")
                    except Exception as e2:
                        print(f"⚠️ ActionChains click failed: {e2}. Trying JS click...")
                        driver.execute_script("arguments[0].click();", link)
                        print("✅ Clicked on visible Opinion link (JS click).")
                clicked = True
                break
            except Exception as e:
                print(f"❌ Failed clicking this link: {e}. Trying next...")
                continue

    if not clicked:
        print("❌ No clickable Opinion link found.")
        driver.quit()
        raise Exception("Could not click any Opinion link")

    time.sleep(5)  # Let the opinion page load fully

    return driver

if __name__ == "__main__":
    driver = get_driver_and_navigate()

