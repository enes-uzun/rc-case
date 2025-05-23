import requests
import json
import time
import sys
import yfinance as yf
from datetime import datetime, timedelta

# Unicode karakterleri Windows'ta bastırabilmek için stdout encoding ayarı
sys.stdout.reconfigure(encoding='utf-8')

# GOOGLE CUSTOM SEARCH AYARLARI
API_KEY = "AIzaSyD4b4Rcd-UQVk_2ND2RQ08vPUxPZxr4Fdc"  # kendi API anahtarın
SEARCH_ENGINE_ID = "60c2410ace77c4a8c"               # kendi arama motoru ID'in

# 🏢 Şirket bilgileri
COMPANIES = {
    "bluedot": {
        "name": "Bluedot",
        "search_terms": ["Bluedot EV charging", "Bluedot electric vehicle payment"],
        "competitors": [
            "TradeStation", "Vajro", "REX", "Logix Net Solutions", 
            "EV Connect", "ChargeHub", "GreenFlux", "Pionix", 
            "ChargeLab", "Electrify America", "EVCS", "Vehya", "PlugShare"
        ]
    },
    "massive_bio": {
        "name": "Massive Bio",
        "search_terms": ["Massive Bio clinical trials", "Massive Bio AI cancer"],
        "competitors": [
            "Deep 6 AI", "Elligo Health Research", "Ancora", "TrialJectory",
            "Antidote", "Oncoshot", "Arctic Therapeutics", "BioPhy",
            "Carenostics", "Admera Health", "Exovera", "Signant Health",
            "Outcomes4Me", "AllStripes", "Leal Health"
        ]
    }
}

# 🔍 Haberleri çeken fonksiyon
def fetch_news(query, company_name):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": 5,
        "safe": "off",
        "hl": "en",
        "gl": "us",
        "dateRestrict": "m1"  # Son 1 ay
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "items" not in data:
            print(f"⚠️  {company_name} için haber bulunamadı")
            return []
            
        return [
            {
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "source": item.get("displayLink", "Unknown")
            }
            for item in data.get("items", [])
        ]
    except Exception as e:
        print(f"❌ {company_name} için haber çekilirken hata: {e}")
        return []

# 📈 Finansal veri çeken fonksiyon (public companies için)
def fetch_financial_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            "symbol": ticker,
            "name": info.get("shortName", "N/A"),
            "current_price": info.get("currentPrice", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "revenue": info.get("totalRevenue", "N/A"),
            "employees": info.get("fullTimeEmployees", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        print(f"❌ {ticker} için finansal veri çekilirken hata: {e}")
        return {"symbol": ticker, "error": str(e)}

# 🎯 Ana veri toplama fonksiyonu
def collect_company_data(company_key, company_info):
    print(f"\n🔍 {company_info['name']} verisi toplanıyor...")
    
    company_data = {
        "name": company_info["name"],
        "collection_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "news": [],
        "competitors": {}
    }
    
    # Ana şirket haberlerini topla
    for search_term in company_info["search_terms"]:
        print(f"  📰 Haber aranıyor: {search_term}")
        news = fetch_news(search_term, company_info["name"])
        company_data["news"].extend(news)
        time.sleep(1)  # Rate limiting
    
    # Competitor haberlerini topla
    for competitor in company_info["competitors"]:
        print(f"  🏢 Competitor: {competitor}")
        competitor_news = fetch_news(f'"{competitor}" news', competitor)
        company_data["competitors"][competitor] = {
            "name": competitor,
            "news": competitor_news
        }
        time.sleep(1)  # Rate limiting
    
    return company_data

# 💾 Verileri kaydetme fonksiyonu
def save_data(all_data):
    # Her şirket için ayrı dosya
    for company_key, data in all_data.items():
        filename = f"{company_key}_data.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ {data['name']} verileri {filename} dosyasına kaydedildi")
    
    # Tüm veriler için genel dosya
    with open("all_company_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    print("✅ Tüm veriler all_company_data.json dosyasına kaydedildi")

# 📊 Data summary fonksiyonu
def print_summary(all_data):
    print("\n" + "="*50)
    print("📊 VERİ TOPLAMA ÖZETİ")
    print("="*50)
    
    for company_key, data in all_data.items():
        print(f"\n🏢 {data['name']}:")
        print(f"   📰 Toplam haber: {len(data['news'])}")
        print(f"   🏭 Competitor sayısı: {len(data['competitors'])}")
        
        total_competitor_news = sum(len(comp['news']) for comp in data['competitors'].values())
        print(f"   📈 Toplam competitor haberi: {total_competitor_news}")

# 🧠 Ana fonksiyon
def main():
    print("🚀 Enhanced Data Collector başlatılıyor...")
    print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_data = {}
    
    for company_key, company_info in COMPANIES.items():
        company_data = collect_company_data(company_key, company_info)
        all_data[company_key] = company_data
    
    # Verileri kaydet
    save_data(all_data)
    
    # Özet göster
    print_summary(all_data)
    
    print("\n🎉 Veri toplama işlemi tamamlandı!")

if __name__ == "__main__":
    main() 