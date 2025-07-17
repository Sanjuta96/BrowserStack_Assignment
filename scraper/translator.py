def translate_with_api(text):
    # MOCK TRANSLATION — swap later with real API
    return text + " (EN)"

def translate_titles(articles):
    return [
        {**art, "title_en": translate_with_api(art["title_es"])}
        for art in articles
    ]
