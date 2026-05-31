// app/tools/bias-scanner/page.tsx
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Loader2, AlertCircle, CheckCircle } from 'lucide-react';

export default function BiasScannerPage() {
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const analyzeBias = async () => {
    setLoading(true);
    
    // Mock response for now (since we'll connect to Python later)
    setTimeout(() => {
      setResult({
        bias_score: 35,
        flagged_phrases: ['rockstar', 'ninja', 'guru', 'work hard play hard'],
        suggestions: {
          'rockstar': 'skilled team member',
          'ninja': 'expert',
          'guru': 'experienced professional'
        },
        rewritten_jd: "We're looking for a skilled team member who collaborates well and delivers quality work..."
      });
      setLoading(false);
    }, 2000);
  };

  const getScoreColor = (score: number) => {
    if (score < 30) return 'text-green-600';
    if (score < 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="max-w-4xl mx-auto py-12 px-4">
      <h1 className="text-3xl font-bold mb-2">JD Bias Scanner</h1>
      <p className="text-gray-600 mb-8">
        Paste your job description to detect exclusionary language and get inclusive alternatives.
      </p>

      <Card>
        <CardHeader>
          <CardTitle>Job Description</CardTitle>
        </CardHeader>
        <CardContent>
          <Textarea
            placeholder="Paste your job description here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows={10}
            className="mb-4"
          />
          <Button 
            onClick={analyzeBias} 
            disabled={loading || !jobDescription}
            size="lg"
            className="w-full md:w-auto"
          >
            {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Analyze for Bias
          </Button>
        </CardContent>
      </Card>

      {result && (
        <div className="mt-8 space-y-6">
          {/* Score Card */}
          <Card>
            <CardHeader>
              <CardTitle>Bias Score</CardTitle>
            </CardHeader>
            <CardContent>
              <div className={`text-5xl font-bold ${getScoreColor(result.bias_score)}`}>
                {result.bias_score}%
              </div>
              <p className="text-gray-600 mt-2">
                {result.bias_score < 30 
                  ? "✅ Great! This JD is fairly inclusive." 
                  : result.bias_score < 60 
                  ? "⚠️ Some bias detected. Review flagged phrases below."
                  : "❌ High bias detected. Consider rewriting using suggestions."}
              </p>
            </CardContent>
          </Card>

          {/* Flagged Phrases */}
          <Card>
            <CardHeader>
              <CardTitle>Flagged Phrases</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {result.flagged_phrases.map((phrase: string, i: number) => (
                  <Badge key={i} variant="destructive" className="text-sm">
                    <AlertCircle className="mr-1 h-3 w-3" />
                    {phrase}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Suggestions */}
          <Card>
            <CardHeader>
              <CardTitle>Inclusive Replacements</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {Object.entries(result.suggestions).map(([bad, good]: [string, any]) => (
                  <div key={bad} className="flex items-start gap-3">
                    <span className="text-red-500 line-through min-w-[100px]">{bad}</span>
                    <span className="text-green-600">→</span>
                    <span className="text-green-700">{good}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Rewritten JD */}
          <Card>
            <CardHeader>
              <CardTitle>Rewritten Job Description</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="bg-gray-50 p-4 rounded-lg whitespace-pre-wrap">
                {result.rewritten_jd}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}