import os, time, requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def save_image(url, path):
    try:
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"✅ Image saved to {path}")
    except Exception as e:
        print(f"⚠️ Failed saving image: {e}")

def scrape_opinion_articles(driver, limit=5):
    driver.get("https://elpais.com")
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))).click()
        print("✅ Cookie accepted.")
    except TimeoutException:
        print("⚠️ Cookie popup not found.")

    opinions = driver.find_elements(By.XPATH, "//a[contains(@href, '/opinion')]")
    for link in opinions:
        if link.is_displayed():
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
            time.sleep(1)
            link.click()
            print("✅ Clicked Opinion link.")
            break

    time.sleep(3)
    info = []
    elems = driver.find_elements(By.CSS_SELECTOR, "article a")[:limit]
    for e in elems:
        href, title = e.get_attribute("href"), e.text.strip()
        if href and title:
            info.append({"href": href, "title_es": title})

    articles = []
    for i, val in enumerate(info, 1):
        driver.get(val["href"])
        time.sleep(2)
        try:
            paras = driver.find_elements(By.CSS_SELECTOR, "div.article_body p")
            content = "\n".join([p.text for p in paras if p.text])
        except:
            content = ""
        try:
            img = driver.find_element(By.CSS_SELECTOR, "figure.article_lead_img img")
            img_url = img.get_attribute("src")
        except:
            img_url = None

        img_path = None
        if img_url:
            img_path = f"screenshots/article_{i}.jpg"
            save_image(img_url, img_path)

        articles.append({
            "title_es": val["title_es"],
            "content_es": content,
            "image_path": img_path
        })

    return articles
