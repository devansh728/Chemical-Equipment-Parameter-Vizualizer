import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { BarChart3 } from 'lucide-react';

interface NumericColumnStats {
  mean: number;
  median: number;
  std: number;
  min: number;
  max: number;
  q1: number;
  q3: number;
  iqr: number;
}

interface StatisticalSummaryProps {
  enhancedSummary: {
    numeric_columns?: Record<string, NumericColumnStats>;
    total_records?: number;
  } | null;
}

export const StatisticalSummary = ({ enhancedSummary }: StatisticalSummaryProps) => {
  if (!enhancedSummary?.numeric_columns) {
    return (
      <Card className="bg-card/80 backdrop-blur-sm border-border/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5" />
            Statistical Summary
          </CardTitle>
          <CardDescription>No statistical data available yet</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Statistical analysis will appear here once the dataset is fully processed.
          </p>
        </CardContent>
      </Card>
    );
  }

  const numericColumns = enhancedSummary.numeric_columns;

  return (
    <Card className="bg-card/80 backdrop-blur-sm border-border/50">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BarChart3 className="w-5 h-5" />
          Statistical Summary
        </CardTitle>
        <CardDescription>
          Detailed statistics for {Object.keys(numericColumns).length} numeric parameters
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="font-semibold">Parameter</TableHead>
                <TableHead className="text-right">Mean</TableHead>
                <TableHead className="text-right">Median</TableHead>
                <TableHead className="text-right">Std Dev</TableHead>
                <TableHead className="text-right">Min</TableHead>
                <TableHead className="text-right">Q1</TableHead>
                <TableHead className="text-right">Q3</TableHead>
                <TableHead className="text-right">Max</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {Object.entries(numericColumns).map(([columnName, stats]) => (
                <TableRow key={columnName}>
                  <TableCell className="font-medium">{columnName}</TableCell>
                  <TableCell className="text-right">{stats.mean.toFixed(2)}</TableCell>
                  <TableCell className="text-right">{stats.median.toFixed(2)}</TableCell>
                  <TableCell className="text-right">{stats.std.toFixed(2)}</TableCell>
                  <TableCell className="text-right">{stats.min.toFixed(2)}</TableCell>
                  <TableCell className="text-right">{stats.q1.toFixed(2)}</TableCell>
                  <TableCell className="text-right">{stats.q3.toFixed(2)}</TableCell>
                  <TableCell className="text-right">{stats.max.toFixed(2)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
        
        {/* Summary Info */}
        <div className="mt-4 pt-4 border-t border-border/50">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <p className="text-muted-foreground">Total Records</p>
              <p className="text-lg font-semibold">{enhancedSummary.total_records || 0}</p>
            </div>
            <div>
              <p className="text-muted-foreground">Numeric Parameters</p>
              <p className="text-lg font-semibold">{Object.keys(numericColumns).length}</p>
            </div>
            <div className="col-span-2">
              <p className="text-muted-foreground text-xs">
                <strong>Note:</strong> Q1 = 25th percentile, Q3 = 75th percentile, IQR = Q3 - Q1
              </p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
