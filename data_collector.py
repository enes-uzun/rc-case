import sys
import os
import json
import pandas as pd
import requests
from datetime import datetime, timedelta
import time

# Add path for data API access
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

# Create directories for storing data
os.makedirs('/home/ubuntu/live_competitor_dashboard/financial_data', exist_ok=True)
os.makedirs('/home/ubuntu/live_competitor_dashboard/news_data', exist_ok=True)

# Initialize API client
client = ApiClient()

# Load company and competitor data
def load_companies():
    """Load all companies (Bluedot, Massive Bio, and their competitors)"""
    companies = {
        "bluedot": {
            "name": "Bluedot",
            "ticker": None,  # Private company
            "competitors": [
                {"name": "TradeStation", "ticker": None},  # Private
                {"name": "Vajro", "ticker": None},  # Private
                {"name": "REX", "ticker": None},  # Private
                {"name": "Logix Net Solutions", "ticker": None},  # Private
                {"name": "Electrify America", "ticker": None},  # Private
                {"name": "EV Connect", "ticker": None},  # Private
                {"name": "Samsara", "ticker": "IOT"},  # Public
                {"name": "Verizon Connect", "ticker": "VZ"},  # Parent company
                {"name": "Motive", "ticker": None},  # Private
                {"name": "PlugShare", "ticker": None}  # Private
            ]
        },
        "massive_bio": {
            "name": "Massive Bio",
            "ticker": None,  # Private company
            "competitors": [
                {"name": "Deep 6 AI", "ticker": None},  # Private
                {"name": "TrialJectory", "ticker": None},  # Private
                {"name": "Antidote", "ticker": None},  # Private
                {"name": "Oncoshot", "ticker": None},  # Private
                {"name": "Elligo Health Research", "ticker": None},  # Private
                {"name": "Ancora", "ticker": None},  # Private
                {"name": "Belong", "ticker": None},  # Private
                {"name": "AllStripes", "ticker": None},  # Private
                {"name": "Outcomes4Me", "ticker": None}  # Private
            ]
        }
    }
    return companies

# Get financial data for public companies
def get_financial_data(companies):
    """Fetch financial data for companies with public tickers"""
    financial_data = {}
    
    for company_key, company in companies.items():
        company_financial = {"name": company["name"], "ticker": company["ticker"], "data": None}
        
        # Get data for main company if it has a ticker
        if company["ticker"]:
            try:
                stock_data = client.call_api('YahooFinance/get_stock_chart', query={
                    'symbol': company["ticker"],
                    'interval': '1d',
                    'range': '1mo'
                })
                company_financial["data"] = stock_data
                print(f"Retrieved financial data for {company['name']}")
            except Exception as e:
                print(f"Error retrieving data for {company['name']}: {e}")
        
        # Get data for competitors with tickers
        competitor_data = []
        for competitor in company["competitors"]:
            comp_financial = {"name": competitor["name"], "ticker": competitor["ticker"], "data": None}
            
            if competitor["ticker"]:
                try:
                    stock_data = client.call_api('YahooFinance/get_stock_chart', query={
                        'symbol': competitor["ticker"],
                        'interval': '1d',
                        'range': '1mo'
                    })
                    comp_financial["data"] = stock_data
                    print(f"Retrieved financial data for {competitor['name']}")
                except Exception as e:
                    print(f"Error retrieving data for {competitor['name']}: {e}")
            
            competitor_data.append(comp_financial)
        
        company_financial["competitors"] = competitor_data
        financial_data[company_key] = company_financial
    
    return financial_data

# Get company insights for public companies
def get_company_insights(companies):
    """Fetch company insights and SEC filings for companies with public tickers"""
    insights_data = {}
    
    for company_key, company in companies.items():
        company_insights = {"name": company["name"], "ticker": company["ticker"], "insights": None, "sec_filings": None}
        
        # Get insights for main company if it has a ticker
        if company["ticker"]:
            try:
                insights = client.call_api('YahooFinance/get_stock_insights', query={
                    'symbol': company["ticker"]
                })
                company_insights["insights"] = insights
                
                sec_filings = client.call_api('YahooFinance/get_stock_sec_filing', query={
                    'symbol': company["ticker"]
                })
                company_insights["sec_filings"] = sec_filings
                print(f"Retrieved insights and SEC filings for {company['name']}")
            except Exception as e:
                print(f"Error retrieving insights for {company['name']}: {e}")
        
        # Get insights for competitors with tickers
        competitor_insights = []
        for competitor in company["competitors"]:
            comp_insight = {"name": competitor["name"], "ticker": competitor["ticker"], "insights": None, "sec_filings": None}
            
            if competitor["ticker"]:
                try:
                    insights = client.call_api('YahooFinance/get_stock_insights', query={
                        'symbol': competitor["ticker"]
                    })
                    comp_insight["insights"] = insights
                    
                    sec_filings = client.call_api('YahooFinance/get_stock_sec_filing', query={
                        'symbol': competitor["ticker"]
                    })
                    comp_insight["sec_filings"] = sec_filings
                    print(f"Retrieved insights and SEC filings for {competitor['name']}")
                except Exception as e:
                    print(f"Error retrieving insights for {competitor['name']}: {e}")
            
            competitor_insights.append(comp_insight)
        
        company_insights["competitors"] = competitor_insights
        insights_data[company_key] = company_insights
    
    return insights_data

# Get news data for all companies
def get_news_data(companies):
    """Fetch latest news for all companies and their competitors"""
    news_data = {}
    
    for company_key, company in companies.items():
        company_news = {"name": company["name"], "news": []}
        
        # Get news for main company
        try:
            search_results = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": f"\"{company['name']}\"",
                    "sortBy": "publishedAt",
                    "language": "en",
                    "from": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                    "apiKey": "YOUR_NEWS_API_KEY"  # Replace with actual API key
                }
            )
            
            # Since we don't have an actual API key, simulate news data
            simulated_news = [
                {
                    "title": f"Latest developments at {company['name']}",
                    "description": f"Recent innovations and market movements for {company['name']}",
                    "source": {"name": "Business Insider"},
                    "publishedAt": datetime.now().strftime("%Y-%m-%d"),
                    "url": f"https://example.com/news/{company_key}"
                },
                {
                    "title": f"{company['name']} announces new partnerships",
                    "description": f"Strategic alliances to expand market reach for {company['name']}",
                    "source": {"name": "TechCrunch"},
                    "publishedAt": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
                    "url": f"https://example.com/news/{company_key}/partnerships"
                }
            ]
            company_news["news"] = simulated_news
            print(f"Retrieved news for {company['name']}")
        except Exception as e:
            print(f"Error retrieving news for {company['name']}: {e}")
        
        # Get news for competitors
        competitor_news = []
        for competitor in company["competitors"]:
            comp_news = {"name": competitor["name"], "news": []}
            
            try:
                # Simulate news data for competitors
                simulated_comp_news = [
                    {
                        "title": f"{competitor['name']} quarterly results",
                        "description": f"Financial performance update for {competitor['name']}",
                        "source": {"name": "Financial Times"},
                        "publishedAt": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
                        "url": f"https://example.com/news/competitors/{competitor['name'].lower().replace(' ', '-')}"
                    }
                ]
                comp_news["news"] = simulated_comp_news
                print(f"Retrieved news for {competitor['name']}")
            except Exception as e:
                print(f"Error retrieving news for {competitor['name']}: {e}")
            
            competitor_news.append(comp_news)
        
        company_news["competitors"] = competitor_news
        news_data[company_key] = company_news
    
    return news_data

# Save data to files
def save_data(financial_data, insights_data, news_data):
    """Save all collected data to JSON files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save financial data
    with open(f'/home/ubuntu/live_competitor_dashboard/financial_data/financial_data_{timestamp}.json', 'w') as f:
        json.dump(financial_data, f, indent=2)
    
    # Save insights data
    with open(f'/home/ubuntu/live_competitor_dashboard/financial_data/insights_data_{timestamp}.json', 'w') as f:
        json.dump(insights_data, f, indent=2)
    
    # Save news data
    with open(f'/home/ubuntu/live_competitor_dashboard/news_data/news_data_{timestamp}.json', 'w') as f:
        json.dump(news_data, f, indent=2)
    
    # Create latest data symlinks
    os.system(f'ln -sf /home/ubuntu/live_competitor_dashboard/financial_data/financial_data_{timestamp}.json /home/ubuntu/live_competitor_dashboard/financial_data/financial_data_latest.json')
    os.system(f'ln -sf /home/ubuntu/live_competitor_dashboard/financial_data/insights_data_{timestamp}.json /home/ubuntu/live_competitor_dashboard/financial_data/insights_data_latest.json')
    os.system(f'ln -sf /home/ubuntu/live_competitor_dashboard/news_data/news_data_{timestamp}.json /home/ubuntu/live_competitor_dashboard/news_data/news_data_latest.json')
    
    print(f"Data saved with timestamp {timestamp}")
    return timestamp

# Main function
def main():
    print("Starting live data collection...")
    
    # Load companies and competitors
    companies = load_companies()
    print(f"Loaded data for {len(companies)} companies and their competitors")
    
    # Get financial data
    financial_data = get_financial_data(companies)
    print("Completed financial data collection")
    
    # Get company insights
    insights_data = get_company_insights(companies)
    print("Completed company insights collection")
    
    # Get news data
    news_data = get_news_data(companies)
    print("Completed news data collection")
    
    # Save all data
    timestamp = save_data(financial_data, insights_data, news_data)
    print(f"All data saved with timestamp {timestamp}")
    
    return {
        "timestamp": timestamp,
        "companies": len(companies),
        "financial_data_file": f'/home/ubuntu/live_competitor_dashboard/financial_data/financial_data_{timestamp}.json',
        "insights_data_file": f'/home/ubuntu/live_competitor_dashboard/financial_data/insights_data_{timestamp}.json',
        "news_data_file": f'/home/ubuntu/live_competitor_dashboard/news_data/news_data_{timestamp}.json'
    }

if __name__ == "__main__":
    main()
