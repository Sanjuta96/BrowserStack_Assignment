# 📰 El País Opinion Article Scraper

This project is a web scraping pipeline built with Python and Selenium that extracts opinion articles from the [El País](https://elpais.com) website. It fetches article titles and content, translates the titles to English (mock translation), analyzes repeated words, and optionally runs tests across multiple devices and browsers using BrowserStack.

---

## 📦 Project Structure

```
el_pais_scraper/
├── Screenshots/                 # Stores captured screenshots and article images
├── scraper/
│   ├── analyzer.py              # Word frequency analysis on translated titles
│   ├── article_scraper.py       # Scrapes opinion articles from elpais.com
│   ├── browserstack_runner.py   # Runs scraping using BrowserStack (single session)
│   ├── parallel_runner.py       # Runs scraping in parallel across multiple devices
│   ├── selenium_setup.py        # Sets up ChromeDriver (local)
│   ├── translator.py            # Mock translation function
│   ├── config.py                # Stores BROWSERSTACK credentials
├── main.py                      # Main runner (local scraping & analysis)
├── requirements.txt             # Dependencies
└── README.md
```

---

## 🚀 Features

- Scrapes **opinion articles** from El País
- Extracts **title, content, and featured image**
- Translates titles from Spanish to English (mock logic)
- Analyzes and displays **frequent words** in translated titles
- Supports local **headless** browser or **BrowserStack** for testing on multiple devices
- Saves screenshots and article images locally

---

## 🛠️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/Sanjuta96/BrowserStack_Assignment.git
cd BrowserStack_Assignment
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **(Optional) Set up BrowserStack credentials**

Create `scraper/config.py` and add:

```python
BROWSERSTACK_USERNAME = "your_username"
BROWSERSTACK_ACCESS_KEY = "your_access_key"
```

---

## 🧪 Usage

### ▶️ Run locally with Chrome

```bash
python main.py
```

This will:

- Launch Chrome (non-headless)
- Scrape 5 opinion articles
- Print Spanish titles and partial content
- Translate titles (mock)
- Analyze repeated English words

### ☁️ Run with BrowserStack (Single Session)

```bash
python scraper/browserstack_runner.py
```

- Scrapes 5 articles and saves a screenshot
- Requires valid BrowserStack credentials

### 🤖 Run in Parallel Across Devices

```bash
python scraper/parallel_runner.py
```

- Launches scraping jobs on Chrome, Edge, Safari, Android, and iOS
- Prints translated titles for each platform

---

## 📊 Output

- **Images** saved to: `Screenshots/article_X.jpg`
- **BrowserStack screenshot** saved to: `Screenshots/browserstack_result.png`
- **Console prints**:
  - Article titles (Spanish + English)
  - First 300 characters of article content
  - Word frequency analysis

---

## 🧪 Example Analysis Output

```text
--- Translated Titles ---
- The democracy debate (EN)
- The democracy debate (EN)
- Europe must act now (EN)
- The democracy debate (EN)

Repeated words in translated headers:
the: 3
democracy: 3
debate: 3
```

---

## 📋 Requirements

- Python 3.7+
- Google Chrome + ChromeDriver
- BrowserStack account (optional)

---

## 📄 License

MIT License

---

## 🙌 Acknowledgements

- [El País](https://elpais.com)
- [Selenium WebDriver](https://www.selenium.dev/)
- [BrowserStack](https://browserstack.com)
