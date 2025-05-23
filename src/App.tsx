import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card";
import { Badge } from "./components/ui/badge";
import companiesData from './data/companies.json';
import './index.css';

interface Development {
  date: string;
  title: string;
  description: string;
}

interface Competitor {
  name: string;
  status: string;
  description: string;
}

interface Company {
  name: string;
  status: string;
  funding: string;
  employees: string;
  founded: string;
  headquarters: string;
  description: string;
  recentDevelopments: Development[];
  competitors: Competitor[];
}

function App() {
  // We're using the state but only through the setter, so we can keep it
  const [, setActiveCompany] = useState<'bluedot' | 'massiveBio'>('bluedot');

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      <header className="bg-white dark:bg-gray-800 shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Competitor Dashboard</h1>
          <p className="text-gray-500 dark:text-gray-400">Live competitor analysis for Revo Capital portfolio companies</p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <Tabs defaultValue="bluedot" onValueChange={(value) => setActiveCompany(value as 'bluedot' | 'massiveBio')} className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-8">
            <TabsTrigger value="bluedot">Bluedot</TabsTrigger>
            <TabsTrigger value="massiveBio">Massive Bio</TabsTrigger>
          </TabsList>
          
          <TabsContent value="bluedot" className="space-y-6">
            <CompanyOverview company={companiesData.bluedot as Company} />
            <RecentDevelopments developments={companiesData.bluedot.recentDevelopments as Development[]} />
            <CompetitorAnalysis competitors={companiesData.bluedot.competitors as Competitor[]} />
          </TabsContent>
          
          <TabsContent value="massiveBio" className="space-y-6">
            <CompanyOverview company={companiesData.massiveBio as Company} />
            <RecentDevelopments developments={companiesData.massiveBio.recentDevelopments as Development[]} />
            <CompetitorAnalysis competitors={companiesData.massiveBio.competitors as Competitor[]} />
          </TabsContent>
        </Tabs>
      </main>
      
      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
        <div className="container mx-auto px-4 py-6">
          <p className="text-center text-gray-500 dark:text-gray-400">
            © {new Date().getFullYear()} Revo Capital Competitor Dashboard. Last updated: {new Date().toLocaleDateString()}
          </p>
        </div>
      </footer>
    </div>
  );
}

function CompanyOverview({ company }: { company: Company }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-2xl">{company.name} Overview</CardTitle>
        <CardDescription>Key company information and metrics</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-medium">Company Profile</h3>
              <p className="text-gray-500 dark:text-gray-400 mt-2">{company.description}</p>
            </div>
            
            <div>
              <h3 className="text-lg font-medium">Headquarters</h3>
              <p className="text-gray-500 dark:text-gray-400 mt-2">{company.headquarters}</p>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <MetricCard title="Status" value={company.status} />
              <MetricCard title="Founded" value={company.founded} />
              <MetricCard title="Funding" value={company.funding} />
              <MetricCard title="Employees" value={company.employees} />
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function MetricCard({ title, value }: { title: string; value: string }) {
  return (
    <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
      <h4 className="text-sm font-medium text-gray-500 dark:text-gray-400">{title}</h4>
      <p className="text-2xl font-bold mt-1">{value}</p>
    </div>
  );
}

function RecentDevelopments({ developments }: { developments: Development[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-2xl">Recent Developments</CardTitle>
        <CardDescription>Latest news and updates</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {developments.map((item, index: number) => (
            <div key={index} className="border-b border-gray-200 dark:border-gray-700 last:border-0 pb-4 last:pb-0">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-medium">{item.title}</h3>
                <Badge variant="outline">{item.date}</Badge>
              </div>
              <p className="text-gray-500 dark:text-gray-400">{item.description}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function CompetitorAnalysis({ competitors }: { competitors: Competitor[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-2xl">Competitor Analysis</CardTitle>
        <CardDescription>Key competitors and their profiles</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {competitors.map((competitor, index: number) => (
            <Card key={index} className="border border-gray-200 dark:border-gray-700">
              <CardHeader className="pb-2">
                <CardTitle>{competitor.name}</CardTitle>
                <Badge variant="outline">{competitor.status}</Badge>
              </CardHeader>
              <CardContent>
                <p className="text-gray-500 dark:text-gray-400 text-sm">{competitor.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

export default App;
