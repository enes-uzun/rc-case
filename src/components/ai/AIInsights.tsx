import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../ui/card";
import { Badge } from "../ui/badge";

interface CompanyData {
  name: string;
  collection_date: string;
  news: any[];
  competitors: Record<string, any>;
}

interface InsightItem {
  title: string;
  description: string;
  priority?: 'high' | 'medium' | 'low';
  severity?: 'high' | 'medium' | 'low';
  strength?: 'strong' | 'moderate' | 'weak';
  effort?: 'low' | 'medium' | 'high';
  actionable?: boolean;
  timeline?: string;
  impact?: 'positive' | 'negative' | 'neutral';
  expected_impact?: 'high' | 'medium' | 'low';
}

interface AIInsightsData {
  opportunities: InsightItem[];
  threats: InsightItem[];
  trends: InsightItem[];
  recommendations: InsightItem[];
  summary: string;
  generated_at: string;
  company: string;
}

interface AIInsightsProps {
  companyData: CompanyData;
  theme?: 'blue' | 'green';
}

export function AIInsights({ companyData, theme = 'blue' }: AIInsightsProps) {
  const [insights, setInsights] = useState<AIInsightsData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const themeColors = {
    blue: {
      primary: 'bg-blue-600 hover:bg-blue-700',
      accent: 'border-blue-500 bg-blue-50',
      text: 'text-blue-600'
    },
    green: {
      primary: 'bg-green-600 hover:bg-green-700',
      accent: 'border-green-500 bg-green-50',
      text: 'text-green-600'
    }
  };

  const colors = themeColors[theme];

  const generateInsights = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/ai/generate-insights', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          company_data: companyData,
          analysis_type: 'full'
        })
      });
      
      if (!response.ok) {
        throw new Error(`AI Service Error: ${response.status}`);
      }
      
      const result = await response.json();
      
      if (result.success) {
        setInsights(result.data);
      } else {
        throw new Error('AI analizi başarısız oldu');
      }
      
    } catch (err) {
      console.error('AI Insights error:', err);
      setError(err instanceof Error ? err.message : 'Bilinmeyen hata');
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getImpactIcon = (impact: string) => {
    switch (impact) {
      case 'positive': return '📈';
      case 'negative': return '📉';
      case 'neutral': return '📊';
      default: return '💡';
    }
  };

  return (
    <Card className={`border-l-4 ${colors.accent}`}>
      <CardHeader>
        <CardTitle className="flex items-center">
          🤖 AI Insights & Analysis
          <Badge className="ml-2 bg-purple-600 text-white">
            GPT-4 Powered
          </Badge>
        </CardTitle>
        <CardDescription>
          {companyData.name} için yapay zeka destekli pazar analizi ve stratejik öneriler
        </CardDescription>
        
        <button 
          onClick={generateInsights}
          disabled={loading}
          className={`mt-4 px-6 py-3 ${colors.primary} text-white rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed`}
        >
          {loading ? (
            <span className="flex items-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              🧠 AI Analizi Yapılıyor...
            </span>
          ) : (
            '🚀 AI Analizi Başlat'
          )}
        </button>
        
        {error && (
          <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-700 text-sm">❌ {error}</p>
            <p className="text-red-600 text-xs mt-1">
              AI service çalışıyor olduğundan ve API anahtarının ayarlandığından emin olun.
            </p>
          </div>
        )}
      </CardHeader>
      
      {insights && (
        <CardContent>
          <div className="space-y-6">
            {/* Summary */}
            <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
              <h3 className="font-semibold text-purple-800 mb-2">📋 Genel Değerlendirme</h3>
              <p className="text-purple-700 text-sm">{insights.summary}</p>
              <p className="text-purple-600 text-xs mt-2">
                🕐 Oluşturulma: {new Date(insights.generated_at).toLocaleString('tr-TR')}
              </p>
            </div>

            {/* Opportunities */}
            <InsightSection 
              title="🎯 Fırsatlar" 
              items={insights.opportunities}
              color="text-green-600"
              getPriorityColor={getPriorityColor}
              priorityKey="priority"
            />
            
            {/* Threats */}
            <InsightSection 
              title="⚠️ Tehditler" 
              items={insights.threats}
              color="text-red-600"
              getPriorityColor={getPriorityColor}
              priorityKey="severity"
            />
            
            {/* Trends */}
            <InsightSection 
              title="📈 Market Trendleri" 
              items={insights.trends}
              color="text-blue-600"
              getPriorityColor={getPriorityColor}
              priorityKey="strength"
              getIcon={getImpactIcon}
              iconKey="impact"
            />
            
            {/* Recommendations */}
            <InsightSection 
              title="💡 Stratejik Öneriler" 
              items={insights.recommendations}
              color="text-purple-600"
              getPriorityColor={getPriorityColor}
              priorityKey="effort"
            />
          </div>
        </CardContent>
      )}
    </Card>
  );
}

interface InsightSectionProps {
  title: string;
  items: InsightItem[];
  color: string;
  getPriorityColor: (priority: string) => string;
  priorityKey: string;
  getIcon?: (key: string) => string;
  iconKey?: string;
}

function InsightSection({ 
  title, 
  items, 
  color, 
  getPriorityColor, 
  priorityKey,
  getIcon,
  iconKey 
}: InsightSectionProps) {
  if (!items || items.length === 0) return null;

  return (
    <div>
      <h3 className={`text-lg font-semibold ${color} mb-3`}>{title}</h3>
      <div className="space-y-3">
        {items.map((item, index) => (
          <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
            <div className="flex items-start justify-between mb-2">
              <h4 className="font-medium text-gray-900 flex items-center">
                {getIcon && iconKey && item[iconKey as keyof InsightItem] && (
                  <span className="mr-2">
                    {getIcon(item[iconKey as keyof InsightItem] as string)}
                  </span>
                )}
                {item.title}
              </h4>
              {item[priorityKey as keyof InsightItem] && (
                <Badge className={getPriorityColor(item[priorityKey as keyof InsightItem] as string)}>
                  {item[priorityKey as keyof InsightItem]}
                </Badge>
              )}
            </div>
            <p className="text-gray-600 text-sm">{item.description}</p>
            
            {/* Additional info */}
            <div className="flex items-center mt-2 space-x-4 text-xs text-gray-500">
              {item.actionable !== undefined && (
                <span className={item.actionable ? 'text-green-600' : 'text-gray-500'}>
                  {item.actionable ? '✅ Aksiyon alınabilir' : '📋 Takip gerekli'}
                </span>
              )}
              {item.timeline && (
                <span>⏰ {item.timeline}</span>
              )}
              {item.expected_impact && (
                <span>🎯 Beklenen etki: {item.expected_impact}</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
} 