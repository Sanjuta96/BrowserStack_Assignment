from selenium.webdriver.common.by import By
import time
import requests
import os


def scrape_articles(driver):
    os.makedirs("screenshots", exist_ok=True)

    # Find articles and extract hrefs upfront to avoid stale references
    articles = driver.find_elements(By.XPATH, "//article//a[contains(@href, '/opinion/')]")[:5]
    links = [article.get_attribute("href") for article in articles]

    data = []

    for idx, link in enumerate(links):
        driver.get(link)
        time.sleep(2)

        title = driver.find_element(By.TAG_NAME, "h1").text.strip()
        paragraphs = driver.find_elements(By.XPATH,
                                          "//div[contains(@class,'article_body') or contains(@class,'articulo-cuerpo')]//p")
        content = "\n".join([p.text for p in paragraphs if p.text.strip()])

        img_url = None
        try:
            img_url = driver.find_element(By.XPATH, "//figure//img").get_attribute("src")
            img_data = requests.get(img_url).content
            with open(f"screenshots/image_{idx + 1}.jpg", "wb") as f:
                f.write(img_data)
        except Exception as e:
            print(f"No image found for article {idx + 1}: {e}")

        data.append({
            'title_es': title,
            'content_es': content,
            'image_url': img_url
        })

    return data
