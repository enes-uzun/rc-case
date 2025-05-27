print("--- Python script ai_service.py STARTING TO LOAD ---")
import openai
import json
import asyncio
import re
from typing import List, Dict, Optional
from datetime import datetime
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# FastAPI app setup
app = FastAPI(title="Competitor AI Analysis Service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsItem(BaseModel):
    title: str
    link: str
    snippet: str
    date: str
    source: str

class CompetitorData(BaseModel):
    name: str
    news: List[NewsItem]

class CompanyData(BaseModel):
    name: str
    collection_date: str
    news: List[NewsItem]
    competitors: Dict[str, CompetitorData]

class AIAnalysisRequest(BaseModel):
    company_data: CompanyData
    analysis_type: str = "full"  # "sentiment", "insights", "trends", "full"

# JSON extraction helper function
def extract_json_from_response(response_text: str) -> Dict:
    """
    OpenAI response'undan JSON'ı çıkarır. Markdown kod blokları ve diğer formatları handle eder.
    """
    try:
        # İlk önce direkt parse etmeyi dene
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    # Markdown kod bloğu içindeki JSON'ı bul
    json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    match = re.search(json_pattern, response_text, re.DOTALL | re.IGNORECASE)
    
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Sadece {} içindeki kısmı al
    brace_pattern = r'\{.*\}'
    match = re.search(brace_pattern, response_text, re.DOTALL)
    
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    
    # Hiçbir şey bulamazsa hata fırlat
    raise json.JSONDecodeError(f"No valid JSON found in response: {response_text[:200]}...", response_text, 0)

class CompetitorAIAnalyzer:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
    
    async def analyze_news_sentiment(self, news_list: List[NewsItem]) -> List[Dict]:
        """Haberlerin sentiment analizini yapar"""
        results = []
        
        for news in news_list:
            try:
                prompt = f"""
                Bu iş haberi için sentiment analizi yap:
                Başlık: {news.title}
                İçerik: {news.snippet}
                Kaynak: {news.source}
                
                JSON formatında şunları döndür:
                {{
                    "sentiment": "positive" | "negative" | "neutral",
                    "confidence": 0.0-1.0,
                    "impact_score": 0-10,
                    "key_insight": "Kısa bir insight (max 100 karakter)",
                    "business_relevance": "high" | "medium" | "low"
                }}
                
                Sadece JSON döndür, başka açıklama yapma.
                """
                
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",  # Cost-effective model
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=200
                )
                
                ai_result = extract_json_from_response(response.choices[0].message.content)
                
                results.append({
                    "title": news.title,
                    "link": news.link,
                    "snippet": news.snippet,
                    "date": news.date,
                    "source": news.source,
                    "sentiment": ai_result.get("sentiment", "neutral"),
                    "confidence": ai_result.get("confidence", 0.5),
                    "impact_score": ai_result.get("impact_score", 5),
                    "key_insight": ai_result.get("key_insight", ""),
                    "business_relevance": ai_result.get("business_relevance", "medium")
                })
                
            except Exception as e:
                print(f"Sentiment analysis error for news: {news.title[:50]}... Error: {e}")
                results.append({
                    "title": news.title,
                    "link": news.link,
                    "snippet": news.snippet,
                    "date": news.date,
                    "source": news.source,
                    "sentiment": "neutral",
                    "confidence": 0.5,
                    "impact_score": 5,
                    "key_insight": "Analiz edilemedi",
                    "business_relevance": "medium"
                })
        
        return results
    
    async def generate_weekly_insights(self, company_data: CompanyData) -> Dict:
        """Haftalık AI insights üretir"""
        try:
            all_news = company_data.news[:10]  # Son 10 haber
            competitor_news = []
            
            for comp_name, comp_data in company_data.competitors.items():
                for news in comp_data.news[:3]:  # Her rakipten 3 haber
                    competitor_news.append({
                        "competitor": comp_name,
                        "title": news.title,
                        "snippet": news.snippet
                    })
            
            prompt = f"""
            {company_data.name} şirketi için iş zekası analisti olarak haftalık insights üret.
            
            Şirket Haberleri ({len(all_news)} adet):
            {json.dumps([{"title": n.title, "snippet": n.snippet[:100]} for n in all_news], indent=2, ensure_ascii=False)}
            
            Rakip Aktiviteleri ({len(competitor_news)} adet):
            {json.dumps(competitor_news[:15], indent=2, ensure_ascii=False)}
            
            Türkçe olarak şu JSON formatında insights üret:
            {{
                "opportunities": [
                    {{"title": "Fırsat başlığı", "description": "Detaylı açıklama", "priority": "high|medium|low", "actionable": true|false}}
                ],
                "threats": [
                    {{"title": "Tehdit başlığı", "description": "Detaylı açıklama", "severity": "high|medium|low", "timeline": "immediate|short-term|long-term"}}
                ],
                "trends": [
                    {{"title": "Trend başlığı", "description": "Açıklama", "strength": "strong|moderate|weak", "impact": "positive|negative|neutral"}}
                ],
                "recommendations": [
                    {{"title": "Öneri başlığı", "description": "Detaylı öneri", "effort": "low|medium|high", "expected_impact": "high|medium|low"}}
                ],
                "summary": "Genel özet (max 200 karakter)"
            }}
            
            Her kategori için 3-5 item üret. Sadece JSON döndür.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1500
            )
            
            insights = extract_json_from_response(response.choices[0].message.content)
            insights["generated_at"] = datetime.now().isoformat()
            insights["company"] = company_data.name
            
            return insights
            
        except Exception as e:
            print(f"Weekly insights generation error: {e}")
            return {
                "opportunities": [{"title": "Analiz Hatası", "description": "AI analizi oluşturulamadı", "priority": "low", "actionable": False}],
                "threats": [],
                "trends": [],
                "recommendations": [],
                "summary": "AI analizi şu anda kullanılamıyor",
                "generated_at": datetime.now().isoformat(),
                "company": company_data.name
            }

# Global analyzer instance
analyzer = None
print("--- Global analyzer initialized to None ---")

@app.on_event("startup")
async def startup_event():
    global analyzer
    print("--- startup_event TRIGGERED ---")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("--- startup_event: OpenAI API key NOT FOUND in env vars. Using fallback. ---")
        api_key = "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" # Bu anahtar muhtemelen geçersiz
    else:
        print(f"--- startup_event: OpenAI API key FOUND in env vars, starting with: {api_key[:8]}...")
    
    if api_key:
        try:
            analyzer = CompetitorAIAnalyzer(api_key)
            print("--- startup_event: CompetitorAIAnalyzer INITIALIZED SUCCESSFULLY ---")
        except Exception as e:
            print(f"--- startup_event: ERROR initializing CompetitorAIAnalyzer: {str(e)} ---")
            analyzer = None
    else:
        print("--- startup_event: No API key available, analyzer remains None ---")
        analyzer = None

@app.get("/")
async def root():
    print(f"--- Request to / received. Analyzer is: {'SET' if analyzer else 'NOT SET'} ---")
    return {"message": "Competitor AI Analysis Service", "status": "running", "version": "1.0.0"}

@app.post("/api/ai/analyze-sentiment")
async def analyze_sentiment(news_items: List[NewsItem]):
    print(f"--- Request to /api/ai/analyze-sentiment received. Analyzer is: {'SET' if analyzer else 'NOT SET'} ---")
    if not analyzer:
        print("--- analyze_sentiment: Analyzer is NOT SET. Raising 503. ---")
        raise HTTPException(status_code=503, detail="AI service not available - check API key")
    
    try:
        results = await analyzer.analyze_news_sentiment(news_items)
        return {"success": True, "data": results, "count": len(results)}
    except Exception as e:
        print(f"--- analyze_sentiment: ERROR during analysis: {str(e)} ---")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/ai/generate-insights")
async def generate_insights(request: AIAnalysisRequest):
    print(f"--- Request to /api/ai/generate-insights received. Analyzer is: {'SET' if analyzer else 'NOT SET'} ---")
    if not analyzer:
        print("--- generate_insights: Analyzer is NOT SET. Raising 503. ---")
        raise HTTPException(status_code=503, detail="AI service not available - check API key")
    
    try:
        insights = await analyzer.generate_weekly_insights(request.company_data)
        return {"success": True, "data": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insights generation failed: {str(e)}")

@app.post("/api/ai/full-analysis")
async def full_analysis(request: AIAnalysisRequest):
    print(f"--- Request to /api/ai/full-analysis received. Analyzer is: {'SET' if analyzer else 'NOT SET'} ---")
    if not analyzer:
        print("--- full_analysis: Analyzer is NOT SET. Raising 503. ---")
        raise HTTPException(status_code=503, detail="AI service not available - check API key")
    
    try:
        # Sentiment analysis
        sentiment_results = await analyzer.analyze_news_sentiment(request.company_data.news)
        
        # Weekly insights
        insights = await analyzer.generate_weekly_insights(request.company_data)
        
        return {
            "success": True,
            "data": {
                "sentiment_analysis": sentiment_results,
                "weekly_insights": insights,
                "analysis_timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full analysis failed: {str(e)}")

print("--- Python script ai_service.py LOADED ---")

# if __name__ == "__main__":
#     import uvicorn
#     print("🚀 Starting Competitor AI Analysis Service...")
#     print("💡 Make sure to set OPENAI_API_KEY environment variable")
#     print("🌐 API will be available at: http://localhost:8001")
#     print("📚 Documentation at: http://localhost:8001/docs")
#     uvicorn.run(app, host="0.0.0.0", port=8001) 