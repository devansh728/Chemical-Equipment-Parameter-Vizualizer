import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Zap, Loader2, TrendingUp, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { dataApi } from '@/lib/api';
import { toast } from 'sonner';

interface OptimizationPanelProps {
  datasetId: number;
  analysisComplete: boolean;
}

interface Optimization {
  title?: string;
  description?: string;
  impact?: 'high' | 'medium' | 'low';
  category?: string;
  estimated_improvement?: string;
}

export function OptimizationPanel({ datasetId, analysisComplete }: OptimizationPanelProps) {
  const [optimizations, setOptimizations] = useState<Optimization[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadOptimizations = async () => {
    if (!analysisComplete) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await dataApi.getOptimizations(datasetId);
      
      if (response.error) {
        setError(response.error);
      } else {
        setOptimizations(response.optimizations || []);
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Failed to load optimization recommendations';
      setError(errorMessage);
      toast.error(errorMessage);
      console.error('Optimization error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (analysisComplete) {
      loadOptimizations();
    }
  }, [datasetId, analysisComplete]);

  const impactColors = {
    high: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    medium: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    low: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
  };

  if (!analysisComplete) {
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Zap className="h-5 w-5 text-yellow-500" />
            <CardTitle>Process Optimization</CardTitle>
          </div>
          <CardDescription>Waiting for analysis to complete...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <AlertCircle className="h-4 w-4" />
            <span>Optimization recommendations will be available after deep analysis completes.</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Zap className="h-5 w-5 text-yellow-500 animate-pulse" />
            <CardTitle>Process Optimization</CardTitle>
          </div>
          <CardDescription>Generating recommendations...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Zap className="h-5 w-5 text-yellow-500" />
            <CardTitle>Process Optimization</CardTitle>
          </div>
          <CardDescription>Error loading recommendations</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
            <Button onClick={loadOptimizations} variant="outline" size="sm">
              Retry
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (optimizations.length === 0) {
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Zap className="h-5 w-5 text-green-500" />
            <CardTitle>Process Optimization</CardTitle>
          </div>
          <CardDescription>Your process is well-optimized</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            No significant optimization opportunities detected. Your equipment parameters appear to be operating efficiently.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Zap className="h-5 w-5 text-yellow-500" />
            <CardTitle>Process Optimization Recommendations</CardTitle>
          </div>
          <Button onClick={loadOptimizations} variant="outline" size="sm">
            Refresh
          </Button>
        </div>
        <CardDescription>
          AI-powered suggestions to improve your chemical process efficiency
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {optimizations.map((opt, index) => {
            const impact = opt.impact || 'medium';

            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="border rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-blue-500" />
                    <h4 className="font-semibold">{opt.title || `Optimization ${index + 1}`}</h4>
                  </div>
                  <Badge className={impactColors[impact]}>
                    {impact} impact
                  </Badge>
                </div>

                {opt.category && (
                  <Badge variant="outline" className="mb-2 text-xs">
                    {opt.category}
                  </Badge>
                )}

                <p className="text-sm text-gray-700 dark:text-gray-300 mb-3">
                  {opt.description || 'No description available'}
                </p>

                {opt.estimated_improvement && (
                  <div className="bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded p-2 mt-2">
                    <div className="flex items-center gap-2 text-xs">
                      <TrendingUp className="h-3 w-3 text-green-600 dark:text-green-400" />
                      <span className="font-semibold text-green-700 dark:text-green-300">
                        Expected Improvement:
                      </span>
                      <span className="text-green-600 dark:text-green-400">
                        {opt.estimated_improvement}
                      </span>
                    </div>
                  </div>
                )}
              </motion.div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
