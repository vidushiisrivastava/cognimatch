// app/tools/culture-report/page.tsx
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2 } from 'lucide-react';

export default function CultureReportPage() {
  const [company, setCompany] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const generateReport = async () => {
    setLoading(true);
    setTimeout(() => {
      setResult({
        inclusion_score: 72,
        strengths: ['Remote work options', 'Flexible hours', 'Mental health days'],
        gaps: ['Lack of neurodiversity training', 'Sensory-unfriendly office'],
        recommendations: [
          'Provide quiet workspaces',
          'Offer communication alternatives (async first)',
          'Train managers on neurodiversity'
        ]
      });
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="max-w-4xl mx-auto py-12 px-4">
      <h1 className="text-3xl font-bold mb-2">Culture Intelligence Report</h1>
      <p className="text-gray-600 mb-8">Get an AI-powered inclusion report for any company.</p>

      <Card>
        <CardHeader>
          <CardTitle>Company Information</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input
            placeholder="Company name"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
          />
          <Textarea
            placeholder="Describe the company culture, work environment, values..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={6}
          />
          <Button onClick={generateReport} disabled={loading || !company} className="w-full">
            {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Generate Report
          </Button>
        </CardContent>
      </Card>

      {result && (
        <div className="mt-8 space-y-4">
          <Card>
            <CardHeader><CardTitle>Inclusion Score</CardTitle></CardHeader>
            <CardContent>
              <div className="text-5xl font-bold text-indigo-600">{result.inclusion_score}%</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle>Strengths</CardTitle></CardHeader>
            <CardContent>
              <ul className="list-disc pl-5">
                {result.strengths.map((s: string, i: number) => <li key={i}>{s}</li>)}
              </ul>
            </CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle>Recommendations</CardTitle></CardHeader>
            <CardContent>
              <ul className="list-disc pl-5">
                {result.recommendations.map((r: string, i: number) => <li key={i}>{r}</li>)}
              </ul>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}