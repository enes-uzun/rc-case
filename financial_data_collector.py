import sys
import os
import json
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime, timedelta
import time

# Create directories for storing data
os.makedirs('/home/ubuntu/competitor_dashboard/financial_data', exist_ok=True)
os.makedirs('/home/ubuntu/competitor_dashboard/news_data', exist_ok=True)

# Function to get financial data for public companies
def get_financial_data(ticker_symbol):
    try:
        # Get stock data
        stock = yf.Ticker(ticker_symbol)
        
        # Basic info
        info = stock.info
        
        # Financial metrics
        financial_data = {
            "symbol": ticker_symbol,
            "name": info.get("shortName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "revenue": info.get("totalRevenue", "N/A"),
            "revenue_growth": info.get("revenueGrowth", "N/A"),
            "profit_margins": info.get("profitMargins", "N/A"),
            "ebitda_margins": info.get("ebitdaMargins", "N/A"),
            "current_price": info.get("currentPrice", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "employees": info.get("fullTimeEmployees", "N/A"),
            "website": info.get("website", "N/A"),
            "description": info.get("longBusinessSummary", "N/A")
        }
        
        # Save to file
        with open(f'/home/ubuntu/competitor_dashboard/financial_data/{ticker_symbol}.json', 'w') as f:
            json.dump(financial_data, f, indent=4)
            
        print(f"Successfully collected financial data for {ticker_symbol}")
        return financial_data
    
    except Exception as e:
        print(f"Error collecting data for {ticker_symbol}: {str(e)}")
        return {"symbol": ticker_symbol, "error": str(e)}

# Function to get news for companies
def get_company_news(company_name, num_articles=5):
    try:
        # Use a news API to get recent news
        # For demonstration, we'll use a simple search approach
        search_term = company_name.replace(" ", "+")
        
        # Get current date and date from 30 days ago
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Format dates for the API
        from_date = start_date.strftime('%Y-%m-%d')
        to_date = end_date.strftime('%Y-%m-%d')
        
        # Collect news through web search
        news_data = {
            "company": company_name,
            "search_term": search_term,
            "date_range": f"{from_date} to {to_date}",
            "articles": []
        }
        
        # Save to file even if empty (will be populated by web search later)
        with open(f'/home/ubuntu/competitor_dashboard/news_data/{company_name.replace(" ", "_")}.json', 'w') as f:
            json.dump(news_data, f, indent=4)
            
        print(f"Created news data file for {company_name}")
        return news_data
    
    except Exception as e:
        print(f"Error collecting news for {company_name}: {str(e)}")
        return {"company": company_name, "error": str(e)}

# Function to get private company data
def get_private_company_data(company_name):
    try:
        # For private companies, we'll create a template to be filled with web research
        private_data = {
            "name": company_name,
            "status": "Private",
            "funding": "To be researched",
            "investors": "To be researched",
            "employees": "To be researched",
            "founded": "To be researched",
            "headquarters": "To be researched",
            "description": "To be researched"
        }
        
        # Save to file
        with open(f'/home/ubuntu/competitor_dashboard/financial_data/{company_name.replace(" ", "_")}.json', 'w') as f:
            json.dump(private_data, f, indent=4)
            
        print(f"Created template for private company data: {company_name}")
        return private_data
    
    except Exception as e:
        print(f"Error creating template for {company_name}: {str(e)}")
        return {"name": company_name, "error": str(e)}

# Define companies and their stock symbols (if public)
bluedot_data = {
    "name": "Bluedot",
    "is_public": False,
    "ticker": None
}

massive_bio_data = {
    "name": "Massive Bio",
    "is_public": False,
    "ticker": None
}

# Define competitors with their stock symbols if public
bluedot_competitors = [
    {"name": "TradeStation", "is_public": False, "ticker": None},
    {"name": "Vajro", "is_public": False, "ticker": None},
    {"name": "REX", "is_public": False, "ticker": None},
    {"name": "Logix Net Solutions", "is_public": False, "ticker": None},
    {"name": "EV Connect", "is_public": False, "ticker": None},
    {"name": "ChargeHub", "is_public": False, "ticker": None},
    {"name": "GreenFlux", "is_public": False, "ticker": None},
    {"name": "Pionix", "is_public": False, "ticker": None},
    {"name": "ChargeLab", "is_public": False, "ticker": None},
    {"name": "Electrify America", "is_public": False, "ticker": None},
    {"name": "EVCS", "is_public": False, "ticker": None},
    {"name": "Vehya", "is_public": False, "ticker": None},
    {"name": "PlugShare", "is_public": False, "ticker": None}
]

massive_bio_competitors = [
    {"name": "Deep 6 AI", "is_public": False, "ticker": None},
    {"name": "Elligo Health Research", "is_public": False, "ticker": None},
    {"name": "Ancora", "is_public": False, "ticker": None},
    {"name": "TrialJectory", "is_public": False, "ticker": None},
    {"name": "Antidote", "is_public": False, "ticker": None},
    {"name": "Oncoshot", "is_public": False, "ticker": None},
    {"name": "Arctic Therapeutics", "is_public": False, "ticker": None},
    {"name": "BioPhy", "is_public": False, "ticker": None},
    {"name": "Carenostics", "is_public": False, "ticker": None},
    {"name": "Admera Health", "is_public": False, "ticker": None},
    {"name": "Exovera", "is_public": False, "ticker": None},
    {"name": "Signant Health", "is_public": False, "ticker": None},
    {"name": "Outcomes4Me", "is_public": False, "ticker": None},
    {"name": "AllStripes", "is_public": False, "ticker": None},
    {"name": "Leal Health", "is_public": False, "ticker": None}
]

# Process main companies
print("Processing main companies...")
if bluedot_data["is_public"] and bluedot_data["ticker"]:
    get_financial_data(bluedot_data["ticker"])
else:
    get_private_company_data(bluedot_data["name"])
get_company_news(bluedot_data["name"])

if massive_bio_data["is_public"] and massive_bio_data["ticker"]:
    get_financial_data(massive_bio_data["ticker"])
else:
    get_private_company_data(massive_bio_data["name"])
get_company_news(massive_bio_data["name"])

# Process Bluedot competitors
print("\nProcessing Bluedot competitors...")
for company in bluedot_competitors:
    if company["is_public"] and company["ticker"]:
        get_financial_data(company["ticker"])
    else:
        get_private_company_data(company["name"])
    get_company_news(company["name"])
    time.sleep(1)  # Avoid rate limiting

# Process Massive Bio competitors
print("\nProcessing Massive Bio competitors...")
for company in massive_bio_competitors:
    if company["is_public"] and company["ticker"]:
        get_financial_data(company["ticker"])
    else:
        get_private_company_data(company["name"])
    get_company_news(company["name"])
    time.sleep(1)  # Avoid rate limiting

print("\nFinancial data and news collection templates created successfully!")
