from collections import Counter

def analyze_titles(articles):
    words = []
    for art in articles:
        t = art.get("title_en","")
        words.extend(t.lower().split())
    freq = Counter(words)
    repeated = {w:c for w,c in freq.items() if c>2}
    print("\nRepeated words in translated headers:")
    if repeated:
        for w,c in repeated.items():
            print(f"{w}: {c}")
    else:
        print("No words repeated more than twice.")
