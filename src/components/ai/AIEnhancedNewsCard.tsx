import React, { useState, useEffect } from 'react';
import { Badge } from "../ui/badge";

interface NewsItem {
  title: string;
  link: string;
  snippet: string;
  date: string;
  source: string;
}

interface NewsWithSentiment extends NewsItem {
  sentiment?: 'positive' | 'negative' | 'neutral';
  confidence?: number;
  impact_score?: number;
  key_insight?: string;
  business_relevance?: 'high' | 'medium' | 'low';
}

interface AIEnhancedNewsCardProps {
  news: NewsItem;
  theme?: 'blue' | 'green';
  enableAI?: boolean;
}

export function AIEnhancedNewsCard({ news, theme = 'blue', enableAI = true }: AIEnhancedNewsCardProps) {
  const [aiAnalysis, setAiAnalysis] = useState<NewsWithSentiment | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const linkColors = {
    blue: 'text-blue-600 hover:text-blue-800',
    green: 'text-green-600 hover:text-green-800'
  };

  const sentimentColors = {
    positive: 'bg-green-100 text-green-800 border-green-200',
    negative: 'bg-red-100 text-red-800 border-red-200',
    neutral: 'bg-gray-100 text-gray-800 border-gray-200'
  };

  const relevanceColors = {
    high: 'bg-red-100 text-red-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-green-100 text-green-800'
  };

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return '😊';
      case 'negative': return '😟';
      case 'neutral': return '😐';
      default: return '🤔';
    }
  };

  const analyzeNews = async () => {
    if (!enableAI) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8001/api/ai/analyze-sentiment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify([{
          title: news.title,
          link: news.link,
          snippet: news.snippet,
          date: news.date,
          source: news.source
        }])
      });
      
      if (!response.ok) {
        throw new Error(`AI Service Error: ${response.status}`);
      }
      
      const result = await response.json();
      
      if (result.success && result.data.length > 0) {
        setAiAnalysis(result.data[0]);
      } else {
        throw new Error('Sentiment analizi başarısız oldu');
      }
      
    } catch (err) {
      console.error('Sentiment analysis error:', err);
      setError('AI analizi kullanılamıyor');
    } finally {
      setLoading(false);
    }
  };

  // Auto-analyze when component mounts
  useEffect(() => {
    if (enableAI) {
      analyzeNews();
    }
  }, [news.title, enableAI]);

  const displayNews = aiAnalysis || news;

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-medium text-lg leading-tight flex-1">
          <a 
            href={news.link} 
            target="_blank" 
            rel="noopener noreferrer"
            className={linkColors[theme]}
          >
            {news.title}
          </a>
        </h3>
        
        <div className="flex flex-col space-y-1 ml-2 shrink-0">
          <Badge variant="outline">{news.source}</Badge>
          
          {/* AI Analysis Badges */}
          {aiAnalysis && (
            <>
              <Badge className={sentimentColors[aiAnalysis.sentiment || 'neutral']}>
                {getSentimentIcon(aiAnalysis.sentiment || 'neutral')} 
                {aiAnalysis.sentiment}
              </Badge>
              
              {aiAnalysis.business_relevance && (
                <Badge className={relevanceColors[aiAnalysis.business_relevance]}>
                  {aiAnalysis.business_relevance} öncelik
                </Badge>
              )}
            </>
          )}
          
          {/* Loading indicator */}
          {loading && enableAI && (
            <Badge className="bg-purple-100 text-purple-800">
              <div className="animate-spin rounded-full h-3 w-3 border-b border-purple-600 mr-1"></div>
              Analiz ediliyor...
            </Badge>
          )}
        </div>
      </div>
      
      <p className="text-gray-600 text-sm mb-2 line-clamp-2">{news.snippet}</p>
      
      {/* AI Analysis Section */}
      {aiAnalysis && !loading && (
        <div className="bg-purple-50 p-3 rounded mt-3 border border-purple-200">
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-sm font-medium text-purple-800">🤖 AI Analizi</h4>
            <div className="flex space-x-2 text-xs">
              {aiAnalysis.confidence !== undefined && (
                <span className="text-purple-600">
                  Güven: {Math.round(aiAnalysis.confidence * 100)}%
                </span>
              )}
              {aiAnalysis.impact_score !== undefined && (
                <span className="text-purple-600">
                  Etki: {aiAnalysis.impact_score}/10
                </span>
              )}
            </div>
          </div>
          
          {aiAnalysis.key_insight && (
            <p className="text-sm text-purple-700 mb-2">
              💡 <strong>Insight:</strong> {aiAnalysis.key_insight}
            </p>
          )}
          
          {/* Visual Impact Score */}
          {aiAnalysis.impact_score !== undefined && (
            <div className="mt-2">
              <div className="flex items-center text-xs text-purple-600 mb-1">
                <span>İş Etkisi:</span>
              </div>
              <div className="w-full bg-purple-200 rounded-full h-2">
                <div 
                  className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${(aiAnalysis.impact_score / 10) * 100}%` }}
                />
              </div>
            </div>
          )}
        </div>
      )}
      
      {/* Error state */}
      {error && enableAI && (
        <div className="bg-red-50 p-2 rounded mt-2 border border-red-200">
          <p className="text-red-700 text-xs">⚠️ {error}</p>
        </div>
      )}
      
      <div className="flex items-center justify-between mt-3">
        <p className="text-xs text-gray-400">{news.date}</p>
        <div className="flex items-center space-x-2">
          <a 
            href={news.link} 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-xs text-blue-500 hover:underline"
          >
            Devamını oku →
          </a>
          
          {enableAI && !aiAnalysis && !loading && (
            <button
              onClick={analyzeNews}
              className="text-xs text-purple-500 hover:text-purple-700 hover:underline"
            >
              🤖 AI Analiz Et
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

// Bulk sentiment analysis for multiple news
export async function bulkAnalyzeNews(newsItems: NewsItem[]): Promise<NewsWithSentiment[]> {
  try {
    const response = await fetch('http://localhost:8001/api/ai/analyze-sentiment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newsItems)
    });
    
    if (!response.ok) {
      throw new Error(`AI Service Error: ${response.status}`);
    }
    
    const result = await response.json();
    
    if (result.success) {
      return result.data;
    } else {
      throw new Error('Bulk sentiment analysis failed');
    }
    
  } catch (error) {
    console.error('Bulk sentiment analysis error:', error);
    return newsItems.map(news => ({
      ...news,
      sentiment: 'neutral' as const,
      confidence: 0.5,
      impact_score: 5,
      key_insight: 'Analiz edilemedi',
      business_relevance: 'medium' as const
    }));
  }
} 