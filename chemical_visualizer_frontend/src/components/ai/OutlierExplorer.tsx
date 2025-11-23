import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { AlertTriangle, HelpCircle, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { useState } from 'react';
import { dataApi } from '@/lib/api';
import { toast } from 'sonner';

interface OutlierExplorerProps {
  outliers: {
    total_outliers?: number;
    outliers_by_parameter?: Record<string, Array<{
      equipment_name: string;
      equipment_type: string;
      value: number;
      expected_range: [number, number];
    }>>;
  } | null;
  datasetId: number;
  loading?: boolean;
}

export function OutlierExplorer({ outliers, datasetId, loading }: OutlierExplorerProps) {
  const [explanations, setExplanations] = useState<Record<string, string>>({});
  const [loadingExplanation, setLoadingExplanation] = useState<string | null>(null);

  const handleExplainOutlier = async (
    parameter: string,
    outlierIndex: number,
    outlierData: any
  ) => {
    const key = `${parameter}-${outlierIndex}`;
    setLoadingExplanation(key);

    try {
      const response = await dataApi.explainOutlier(datasetId, {
        equipment_name: outlierData.equipment_name,
        equipment_type: outlierData.equipment_type,
        parameter: parameter,
        value: outlierData.value,
        expected_range: outlierData.expected_range
      });

      setExplanations(prev => ({
        ...prev,
        [key]: response.explanation
      }));
    } catch (error) {
      toast.error('Failed to get explanation. Please try again.');
      console.error('Explanation error:', error);
    } finally {
      setLoadingExplanation(null);
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-orange-500 animate-pulse" />
            <CardTitle>Outlier Detection</CardTitle>
          </div>
          <CardDescription>Analyzing anomalies...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 animate-pulse">
            <div className="h-16 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div className="h-16 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!outliers || !outliers.outliers_by_parameter || outliers.total_outliers === 0) {
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-green-500" />
            <CardTitle>Outlier Detection</CardTitle>
          </div>
          <CardDescription>No outliers detected</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            All equipment parameters are within expected ranges. No anomalies found.
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
            <AlertTriangle className="h-5 w-5 text-orange-500" />
            <CardTitle>Outlier Detection</CardTitle>
          </div>
          <Badge variant="destructive">
            {outliers.total_outliers} Anomalies Found
          </Badge>
        </div>
        <CardDescription>
          Equipment parameters outside expected ranges (IQR method)
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {Object.entries(outliers.outliers_by_parameter).map(([parameter, paramOutliers], paramIndex) => (
            <motion.div
              key={parameter}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: paramIndex * 0.1 }}
              className="border rounded-lg p-4"
            >
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-semibold text-sm flex items-center gap-2">
                  <AlertTriangle className="h-4 w-4 text-orange-500" />
                  {parameter}
                </h4>
                <Badge variant="outline">{paramOutliers.length} outliers</Badge>
              </div>

              <div className="space-y-3">
                {paramOutliers.map((outlier, outlierIndex) => {
                  const key = `${parameter}-${outlierIndex}`;
                  const hasExplanation = explanations[key];
                  const isLoading = loadingExplanation === key;

                  return (
                    <div
                      key={outlierIndex}
                      className="bg-orange-50 dark:bg-orange-950 border border-orange-200 dark:border-orange-800 rounded p-3"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <div className="font-medium text-sm">
                            {outlier.equipment_name}
                          </div>
                          <div className="text-xs text-gray-600 dark:text-gray-400">
                            {outlier.equipment_type}
                          </div>
                        </div>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleExplainOutlier(parameter, outlierIndex, outlier)}
                          disabled={isLoading}
                          className="text-xs"
                        >
                          {isLoading ? (
                            <>
                              <Loader2 className="h-3 w-3 mr-1 animate-spin" />
                              Analyzing...
                            </>
                          ) : (
                            <>
                              <HelpCircle className="h-3 w-3 mr-1" />
                              Explain
                            </>
                          )}
                        </Button>
                      </div>

                      <div className="grid grid-cols-2 gap-2 text-xs mb-2">
                        <div>
                          <span className="text-gray-600 dark:text-gray-400">Value:</span>
                          <span className="ml-1 font-mono font-semibold text-orange-600 dark:text-orange-400">
                            {outlier.value.toFixed(2)}
                          </span>
                        </div>
                        <div>
                          <span className="text-gray-600 dark:text-gray-400">Expected:</span>
                          <span className="ml-1 font-mono">
                            [{outlier.expected_range[0].toFixed(2)}, {outlier.expected_range[1].toFixed(2)}]
                          </span>
                        </div>
                      </div>

                      {hasExplanation && (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          className="mt-3 pt-3 border-t border-orange-200 dark:border-orange-800"
                        >
                          <div className="text-xs text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-900 p-2 rounded">
                            <strong className="text-purple-600 dark:text-purple-400">AI Explanation:</strong>
                            <p className="mt-1">{explanations[key]}</p>
                          </div>
                        </motion.div>
                      )}
                    </div>
                  );
                })}
              </div>
            </motion.div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
