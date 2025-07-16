from scraper.selenium_setup import get_driver_and_navigate
from scraper.article_scraper import scrape_articles
from scraper.translator import translate_titles
from scraper.analyzer import analyze_titles

# Step 1: Setup driver and go to Opinion section
driver = get_driver_and_navigate()

# Step 2: Scrape first 5 articles
articles = scrape_articles(driver)
driver.quit()

# Step 3: Translate titles
translated_articles = translate_titles(articles)

# Step 4: Analyze translated titles
analyze_titles(translated_articles)
