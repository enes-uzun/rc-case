export interface NewsItem {
  title: string;
  link: string;
  snippet: string;
  date: string;
  source: string;
}

export interface NewsWithSentiment extends NewsItem {
  sentiment?: 'positive' | 'negative' | 'neutral';
  confidence?: number;
  impact_score?: number;
  key_insight?: string;
  business_relevance?: 'high' | 'medium' | 'low';
}

export async function bulkAnalyzeNews(newsItems: NewsItem[]): Promise<NewsWithSentiment[]> {
  try {
    const response = await fetch('/api/ai/analyze-sentiment', {
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