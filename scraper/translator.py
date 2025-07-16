from deep_translator import GoogleTranslator

def translate_titles(articles):
    for article in articles:
        translation = GoogleTranslator(source='es', target='en').translate(article['title_es'])
        article['title_en'] = translation
        print(f"\nOriginal: {article['title_es']}\nTranslated: {article['title_en']}")
    return articles
