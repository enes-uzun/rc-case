import requests
import json
import time
import sys

# Unicode karakterleri Windows'ta bastırabilmek için stdout encoding ayarı
sys.stdout.reconfigure(encoding='utf-8')

# GOOGLE CUSTOM SEARCH AYARLARI
API_KEY = "AIzaSyD4b4Rcd-UQVk_2ND2RQ08vPUxPZxr4Fdc"  # kendi API anahtarın
SEARCH_ENGINE_ID = "60c2410ace77c4a8c"               # kendi arama motoru ID'in

# 🔍 Haberleri çeken fonksiyon
def fetch_news(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": 5,
        "safe": "off",
        "hl": "en",
        "gl": "us"
    }

    response = requests.get(url, params=params)
    
    try:
        data = response.json()
    except json.JSONDecodeError:
        print("JSON decode error. Yanıt alınamadı.")
        return []

    return [
        {
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        }
        for item in data.get("items", [])
    ]


# 🧠 Ana fonksiyon
def main():
    companies = [
        "Deep 6 AI",
        "Elligo Health Research",
        "Ancora",
        "Perthera",
        "Leal Health"
    ]

    all_results = {}

    for company in companies:
        print(f"🔍 Haber aranıyor: {company}")
        query = f'"{company}" clinical trials'
        results = fetch_news(query)
        all_results[company] = results
        time.sleep(1)  # rate limit'e yakalanmamak için küçük gecikme

    # JSON dosyasına kaydet
    with open("competitor_news.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print("Haberler competitor_news.json dosyasına kaydedildi.")


if __name__ == "__main__":
    main()
