from collections import Counter

def analyze_titles(articles):
    words = []
    for article in articles:
        words += article['title_en'].lower().split()

    counter = Counter(words)
    repeated = {word: count for word, count in counter.items() if count > 2}

    print("\nRepeated words in translated headers:")
    for word, count in repeated.items():
        print(f"{word}: {count}")
