import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./src/components/ui/card";
import { Badge } from "./src/components/ui/badge";

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

export function DataIntegration() {
  const [companyData, setCompanyData] = useState<AllCompanyData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadCompanyData();
  }, []);

  const loadCompanyData = async () => {
    try {
      // Enhanced data collector'dan gelen dosyayı yükle
      const response = await fetch('/all_company_data.json');
      if (!response.ok) {
        throw new Error('Veri yüklenemedi');
      }
      const data = await response.json();
      setCompanyData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Bilinmeyen hata');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-lg">📊 Veriler yükleniyor...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-red-500">❌ Hata: {error}</div>
      </div>
    );
  }

  if (!companyData) {
    return null;
  }

  return (
    <div className="space-y-8">
      {/* Bluedot Section */}
      <CompanySection 
        company={companyData.bluedot} 
        title="Bluedot - EV Charging Platform"
        accent="blue"
      />
      
      {/* Massive Bio Section */}
      <CompanySection 
        company={companyData.massive_bio} 
        title="Massive Bio - AI Clinical Trials"
        accent="green"
      />
    </div>
  );
}

interface CompanySectionProps {
  company: CompanyData;
  title: string;
  accent: 'blue' | 'green';
}

function CompanySection({ company, title, accent }: CompanySectionProps) {
  const accentColors = {
    blue: 'border-blue-500 bg-blue-50',
    green: 'border-green-500 bg-green-50'
  };

  return (
    <div className={`border-l-4 ${accentColors[accent]} p-6 rounded-r-lg`}>
      <h2 className="text-2xl font-bold mb-4">{title}</h2>
      <p className="text-sm text-gray-500 mb-6">
        Son güncelleme: {company.collection_date}
      </p>

      {/* Recent News */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>📰 Son Haberler ({company.news.length})</CardTitle>
          <CardDescription>
            {company.name} hakkında son haberler
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {company.news.slice(0, 5).map((news, index) => (
              <NewsCard key={index} news={news} />
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Competitors Overview */}
      <Card>
        <CardHeader>
          <CardTitle>
            🏢 Rakip Analizi ({Object.keys(company.competitors).length} şirket)
          </CardTitle>
          <CardDescription>
            Rakip şirketlerden son haberler
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(company.competitors).map(([key, competitor]) => (
              <CompetitorCard key={key} competitor={competitor} />
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function NewsCard({ news }: { news: NewsItem }) {
  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-medium text-lg leading-tight">
          <a 
            href={news.link} 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800"
          >
            {news.title}
          </a>
        </h3>
        <Badge variant="outline" className="ml-2 shrink-0">
          {news.source}
        </Badge>
      </div>
      <p className="text-gray-600 text-sm mb-2">{news.snippet}</p>
      <p className="text-xs text-gray-400">{news.date}</p>
    </div>
  );
}

function CompetitorCard({ competitor }: { competitor: CompetitorData }) {
  const [isExpanded, setIsExpanded] = React.useState(false);
  const newsCount = competitor.news.length;
  
  const displayedNews = isExpanded ? competitor.news : competitor.news.slice(0, 2);
  const remainingCount = newsCount - 2;
  
  return (
    <Card className="h-full">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg">{competitor.name}</CardTitle>
        <Badge variant={newsCount > 0 ? "default" : "secondary"}>
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
                  className="text-blue-600 hover:text-blue-800 line-clamp-2"
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
          <p className="text-sm text-gray-500">Son dönemde haber bulunamadı</p>
        )}
      </CardContent>
    </Card>
  );
} 