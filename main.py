from scraper.selenium_setup import get_driver
from scraper.article_scraper import scrape_opinion_articles
from scraper.translator import translate_titles
from scraper.analyzer import analyze_titles

def main():
    driver = get_driver(headless=False)
    articles = scrape_opinion_articles(driver)
    driver.quit()

    print("\n--- Spanish Titles & Content ---")
    for i, art in enumerate(articles, 1):
        print(f"\nArticle {i}")
        print(f"Title (ES): {art['title_es']}")
        print(f"Content (ES):\n{art['content_es'][:300]}...")

    translated = translate_titles(articles)
    print("\n--- Translated Titles ---")
    for art in translated:
        print(f"- {art['title_en']}")

    analyze_titles(translated)

if __name__=="__main__":
    main()
