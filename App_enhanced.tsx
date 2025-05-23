import React, { useState, useEffect } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./src/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./src/components/ui/card";
import { Badge } from "./src/components/ui/badge";
import { AIInsights } from "./src/components/ai/AIInsights";
import { AIEnhancedNewsCard } from "./src/components/ai/AIEnhancedNewsCard";
import './index.css';

interface NewsItem {
  title: string;
  link: string;
  snippet: string;
  date: string;
  source: string;
}

interface CompetitorData {
  name: string;
  news: NewsItem[];
}

interface CompanyData {
  name: string;
  collection_date: string;
  news: NewsItem[];
  competitors: Record<string, CompetitorData>;
}

interface AllCompanyData {
  bluedot: CompanyData;
  massive_bio: CompanyData;
}

function App() {
  const [companyData, setCompanyData] = useState<AllCompanyData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'bluedot' | 'massive_bio'>('bluedot');

  useEffect(() => {
    loadCompanyData();
  }, []);

  const loadCompanyData = async () => {
    try {
      // all_company_data.json dosyasını yükle
      const response = await fetch('./all_company_data.json');
      if (!response.ok) {
        throw new Error('Veri dosyası bulunamadı');
      }
      const data = await response.json();
      setCompanyData(data);
    } catch (err) {
      console.error('Veri yükleme hatası:', err);
      setError(err instanceof Error ? err.message : 'Bilinmeyen hata');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <div className="text-lg font-medium">📊 Canlı veriler yükleniyor...</div>
          <div className="text-sm text-gray-500 mt-2">Enhanced Data Collector verileri</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">❌</div>
          <div className="text-xl font-medium text-red-600">Veri Yükleme Hatası</div>
          <div className="text-gray-500 mt-2">{error}</div>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Tekrar Dene
          </button>
        </div>
      </div>
    );
  }

  if (!companyData) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                🚀 Enhanced Competitor Dashboard
              </h1>
              <p className="text-gray-500 dark:text-gray-400 mt-1">
                Revo Capital portföy şirketleri için canlı rakip analizi
              </p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500">Son Güncelleme</div>
              <div className="text-sm font-medium">
                {companyData[activeTab]?.collection_date}
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <Tabs 
          defaultValue="bluedot" 
          onValueChange={(value) => setActiveTab(value as 'bluedot' | 'massive_bio')} 
          className="w-full"
        >
          <TabsList className="grid w-full grid-cols-2 mb-8">
            <TabsTrigger value="bluedot" className="text-lg">
              ⚡ Bluedot ({companyData.bluedot.news.length} haber)
            </TabsTrigger>
            <TabsTrigger value="massive_bio" className="text-lg">
              🧬 Massive Bio ({companyData.massive_bio.news.length} haber)
            </TabsTrigger>
          </TabsList>
          
          <TabsContent value="bluedot" className="space-y-6">
            <CompanyDashboard 
              company={companyData.bluedot} 
              theme="blue"
              description="EV şarj ödeme platformu - Elektrikli araç filolarına kesintisiz şarj erişimi"
            />
          </TabsContent>
          
          <TabsContent value="massive_bio" className="space-y-6">
            <CompanyDashboard 
              company={companyData.massive_bio} 
              theme="green"
              description="AI destekli klinik deneyim eşleştirme - Kanser hastalarını uygun klinik denemelerle buluşturuyor"
            />
          </TabsContent>
        </Tabs>
      </main>
      
      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <p className="text-gray-500 dark:text-gray-400">
              © {new Date().getFullYear()} Revo Capital Enhanced Dashboard
            </p>
            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <span>🔄 Otomatik güncelleme: 6 saatte bir</span>
              <span>📡 Google Custom Search API</span>
              <span>🎯 {Object.keys(companyData.bluedot.competitors).length + Object.keys(companyData.massive_bio.competitors).length} rakip takip ediliyor</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

interface CompanyDashboardProps {
  company: CompanyData;
  theme: 'blue' | 'green';
  description: string;
}

function CompanyDashboard({ company, theme, description }: CompanyDashboardProps) {
  const themeColors = {
    blue: {
      accent: 'border-blue-500 bg-blue-50',
      primary: 'text-blue-600',
      bg: 'bg-blue-500'
    },
    green: {
      accent: 'border-green-500 bg-green-50',
      primary: 'text-green-600',
      bg: 'bg-green-500'
    }
  };

  const colors = themeColors[theme];

  return (
    <div className="space-y-6">
      {/* Company Overview */}
      <Card className={`border-l-4 ${colors.accent}`}>
        <CardHeader>
          <CardTitle className="text-2xl">{company.name} Genel Bakış</CardTitle>
          <CardDescription>{description}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <MetricCard 
              title="Son Haberler" 
              value={company.news.length.toString()} 
              subtitle="Son 1 ay"
              color={colors.primary}
            />
            <MetricCard 
              title="Takip Edilen Rakipler" 
              value={Object.keys(company.competitors).length.toString()} 
              subtitle="Aktif monitoring"
              color={colors.primary}
            />
            <MetricCard 
              title="Toplam Rakip Haberi" 
              value={Object.values(company.competitors).reduce((total, comp) => total + comp.news.length, 0).toString()}
              subtitle="Son dönem"
              color={colors.primary}
            />
          </div>
        </CardContent>
      </Card>

      {/* AI Insights - NEW SECTION */}
      <AIInsights companyData={company} theme={theme} />

      {/* Recent News with AI Enhancement */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            📰 {company.name} - AI-Enhanced Haberler 
            <Badge className={`ml-2 ${colors.bg} text-white`}>
              {company.news.length} haber
            </Badge>
            <Badge className="ml-2 bg-purple-600 text-white">
              🤖 AI Powered
            </Badge>
          </CardTitle>
          <CardDescription>
            Yapay zeka destekli sentiment analizi ile gerçek zamanlı haber takibi
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {company.news.slice(0, 8).map((news, index) => (
              <AIEnhancedNewsCard 
                key={index} 
                news={news} 
                theme={theme}
                enableAI={true}
              />
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Competitors Analysis */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            🏢 Rakip Analizi 
            <Badge className={`ml-2 ${colors.bg} text-white`}>
              {Object.keys(company.competitors).length} şirket
            </Badge>
          </CardTitle>
          <CardDescription>
            Rakip şirketlerden gerçek zamanlı haber takibi
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(company.competitors).map(([key, competitor]) => (
              <CompetitorCard key={key} competitor={competitor} theme={theme} />
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function MetricCard({ title, value, subtitle, color }: { 
  title: string; 
  value: string; 
  subtitle: string;
  color: string;
}) {
  return (
    <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
      <h4 className="text-sm font-medium text-gray-500 dark:text-gray-400">{title}</h4>
      <p className={`text-3xl font-bold mt-1 ${color}`}>{value}</p>
      <p className="text-xs text-gray-400 mt-1">{subtitle}</p>
    </div>
  );
}

function NewsCard({ news, theme }: { news: NewsItem; theme: 'blue' | 'green' }) {
  const linkColor = theme === 'blue' ? 'text-blue-600 hover:text-blue-800' : 'text-green-600 hover:text-green-800';
  
  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-medium text-lg leading-tight flex-1">
          <a 
            href={news.link} 
            target="_blank" 
            rel="noopener noreferrer"
            className={linkColor}
          >
            {news.title}
          </a>
        </h3>
        <Badge variant="outline" className="ml-2 shrink-0">
          {news.source}
        </Badge>
      </div>
      <p className="text-gray-600 text-sm mb-2 line-clamp-2">{news.snippet}</p>
      <div className="flex items-center justify-between">
        <p className="text-xs text-gray-400">{news.date}</p>
        <a 
          href={news.link} 
          target="_blank" 
          rel="noopener noreferrer"
          className="text-xs text-blue-500 hover:underline"
        >
          Devamını oku →
        </a>
      </div>
    </div>
  );
}

function CompetitorCard({ competitor, theme }: { competitor: CompetitorData; theme: 'blue' | 'green' }) {
  const [isExpanded, setIsExpanded] = React.useState(false);
  const newsCount = competitor.news.length;
  const badgeColor = theme === 'blue' ? 'bg-blue-500' : 'bg-green-500';
  
  const displayedNews = isExpanded ? competitor.news : competitor.news.slice(0, 2);
  const remainingCount = newsCount - 2;
  
  return (
    <Card className="h-full">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg">{competitor.name}</CardTitle>
        <Badge className={`${badgeColor} text-white w-fit`}>
          {newsCount} haber
        </Badge>
      </CardHeader>
      <CardContent>
        {newsCount > 0 ? (
          <div className="space-y-2">
            {displayedNews.map((news, index) => (
              <div key={index} className="text-sm">
                <a 
                  href={news.link} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 line-clamp-2 block"
                >
                  {news.title}
                </a>
                <p className="text-xs text-gray-400 mt-1">{news.date}</p>
              </div>
            ))}
            {newsCount > 2 && (
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="text-xs text-blue-500 hover:text-blue-700 font-medium cursor-pointer hover:underline w-full text-left"
              >
                {isExpanded 
                  ? '▲ Daha az göster' 
                  : `▼ +${remainingCount} daha fazla haber göster`
                }
              </button>
            )}
          </div>
        ) : (
          <p className="text-sm text-gray-500 italic">Son dönemde haber bulunamadı</p>
        )}
      </CardContent>
    </Card>
  );
}

export default App; 