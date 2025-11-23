import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Lightbulb, TrendingUp, BarChart3, PieChart } from 'lucide-react';
import { motion } from 'framer-motion';

interface SmartSuggestionsProps {
  suggestions: {
    suggestions?: Array<{
      chart_type?: string;
      parameters?: string[];
      reason?: string;
      priority?: 'high' | 'medium' | 'low';
    }>;
  } | null;
  loading?: boolean;
}

const chartIcons = {
  scatter: BarChart3,
  bar: BarChart3,
  line: TrendingUp,
  pie: PieChart,
  heatmap: BarChart3,
  default: BarChart3
};

const priorityColors = {
  high: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  medium: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  low: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
};

export function SmartSuggestions({ suggestions, loading }: SmartSuggestionsProps) {
  if (loading) {
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Lightbulb className="h-5 w-5 text-yellow-500 animate-pulse" />
            <CardTitle>Smart Analysis Suggestions</CardTitle>
          </div>
          <CardDescription>Generating recommendations...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4 animate-pulse">
            <div className="h-20 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div className="h-20 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!suggestions || !suggestions.suggestions || suggestions.suggestions.length === 0) {
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Lightbulb className="h-5 w-5 text-yellow-500" />
            <CardTitle>Smart Analysis Suggestions</CardTitle>
          </div>
          <CardDescription>No suggestions available yet</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-2">
          <Lightbulb className="h-5 w-5 text-yellow-500" />
          <CardTitle>Smart Analysis Suggestions</CardTitle>
        </div>
        <CardDescription>AI-recommended visualizations for your dataset</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {suggestions.suggestions.map((suggestion, index) => {
            const ChartIcon = chartIcons[suggestion.chart_type as keyof typeof chartIcons] || chartIcons.default;
            const priority = suggestion.priority || 'medium';

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
                    <ChartIcon className="h-5 w-5 text-blue-500" />
                    <h4 className="font-semibold capitalize">
                      {suggestion.chart_type?.replace('_', ' ') || 'Analysis'}
                    </h4>
                  </div>
                  <Badge className={priorityColors[priority]}>
                    {priority}
                  </Badge>
                </div>

                {suggestion.parameters && suggestion.parameters.length > 0 && (
                  <div className="mb-2">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Parameters: </span>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {suggestion.parameters.map((param, i) => (
                        <Badge key={i} variant="outline" className="text-xs">
                          {param}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {suggestion.reason && (
                  <p className="text-sm text-gray-700 dark:text-gray-300 mt-2">
                    {suggestion.reason}
                  </p>
                )}
              </motion.div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
