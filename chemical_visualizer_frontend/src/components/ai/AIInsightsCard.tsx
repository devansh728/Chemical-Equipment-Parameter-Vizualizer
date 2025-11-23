import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Sparkles, AlertTriangle, CheckCircle, Info } from 'lucide-react';
import { motion } from 'framer-motion';

interface AIInsightsCardProps {
  aiInsights: {
    executive_summary?: string;
    risk_level?: 'low' | 'medium' | 'high' | 'critical' | 'unknown';
    recommendations?: string[];
    key_findings?: string[];
  } | null;
  loading?: boolean;
}

const riskConfig = {
  low: { color: 'bg-green-500', icon: CheckCircle, label: 'Low Risk' },
  medium: { color: 'bg-yellow-500', icon: Info, label: 'Medium Risk' },
  high: { color: 'bg-orange-500', icon: AlertTriangle, label: 'High Risk' },
  critical: { color: 'bg-red-500', icon: AlertTriangle, label: 'Critical Risk' },
  unknown: { color: 'bg-gray-500', icon: Info, label: 'Unknown' }
};

export function AIInsightsCard({ aiInsights, loading }: AIInsightsCardProps) {
  if (loading) {
    return (
      <Card className="border-purple-200 dark:border-purple-800">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-purple-500 animate-pulse" />
            <CardTitle>AI Insights</CardTitle>
          </div>
          <CardDescription>Generating AI-powered analysis...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4 animate-pulse">
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-full"></div>
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-2/3"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!aiInsights || !aiInsights.executive_summary) {
    return (
      <Card className="border-purple-200 dark:border-purple-800">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-purple-500" />
            <CardTitle>AI Insights</CardTitle>
          </div>
          <CardDescription>AI analysis unavailable</CardDescription>
        </CardHeader>
        <CardContent>
          <Alert>
            <Info className="h-4 w-4" />
            <AlertDescription>
              AI insights are being generated. Please wait for the analysis to complete.
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    );
  }

  const riskLevel = aiInsights.risk_level || 'unknown';
  const RiskIcon = riskConfig[riskLevel].icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="border-purple-200 dark:border-purple-800 shadow-lg">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-purple-500" />
              <CardTitle>AI Executive Summary</CardTitle>
            </div>
            <Badge className={`${riskConfig[riskLevel].color} text-white`}>
              <RiskIcon className="h-3 w-3 mr-1" />
              {riskConfig[riskLevel].label}
            </Badge>
          </div>
          <CardDescription>AI-powered analysis of your chemical equipment data</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Executive Summary */}
          <div>
            <h3 className="font-semibold text-sm text-gray-600 dark:text-gray-400 mb-2">
              Summary
            </h3>
            <p className="text-sm leading-relaxed">{aiInsights.executive_summary}</p>
          </div>

          {/* Key Findings */}
          {aiInsights.key_findings && aiInsights.key_findings.length > 0 && (
            <div>
              <h3 className="font-semibold text-sm text-gray-600 dark:text-gray-400 mb-2">
                Key Findings
              </h3>
              <ul className="space-y-2">
                {aiInsights.key_findings.map((finding, index) => (
                  <motion.li
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-start gap-2 text-sm"
                  >
                    <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                    <span>{finding}</span>
                  </motion.li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommendations */}
          {aiInsights.recommendations && aiInsights.recommendations.length > 0 && (
            <div>
              <h3 className="font-semibold text-sm text-gray-600 dark:text-gray-400 mb-2">
                Recommendations
              </h3>
              <ul className="space-y-2">
                {aiInsights.recommendations.map((rec, index) => (
                  <motion.li
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 + 0.2 }}
                    className="flex items-start gap-2 text-sm"
                  >
                    <Info className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                    <span>{rec}</span>
                  </motion.li>
                ))}
              </ul>
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
