import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useMemo } from 'react';
import { motion } from 'framer-motion';

interface CorrelationHeatmapProps {
  correlationData: {
    correlation_matrix?: number[][];
    column_names?: string[];
    strong_correlations?: Array<{
      param1: string;
      param2: string;
      coefficient: number;
    }>;
  } | null;
  loading?: boolean;
}

export function CorrelationHeatmap({ correlationData, loading }: CorrelationHeatmapProps) {
  const getColorForValue = (value: number): string => {
    // Map correlation coefficient (-1 to 1) to color
    const intensity = Math.abs(value);
    if (value > 0) {
      // Positive correlation: blue shades
      return `rgba(59, 130, 246, ${intensity})`;
    } else {
      // Negative correlation: red shades
      return `rgba(239, 68, 68, ${intensity})`;
    }
  };

  const cellSize = useMemo(() => {
    if (!correlationData?.column_names) return 60;
    const numCols = correlationData.column_names.length;
    if (numCols > 10) return 40;
    if (numCols > 6) return 50;
    return 60;
  }, [correlationData]);

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Correlation Heatmap</CardTitle>
          <CardDescription>Loading correlation analysis...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-64 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        </CardContent>
      </Card>
    );
  }

  if (!correlationData || !correlationData.correlation_matrix || !correlationData.column_names) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Correlation Heatmap</CardTitle>
          <CardDescription>No correlation data available</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-gray-500">
            Correlation analysis requires numerical parameters in your dataset.
          </p>
        </CardContent>
      </Card>
    );
  }

  const { correlation_matrix, column_names, strong_correlations } = correlationData;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Parameter Correlation Heatmap</CardTitle>
        <CardDescription>
          Pearson correlation coefficients between numerical parameters
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Heatmap */}
          <div className="overflow-x-auto">
            <div className="inline-block min-w-full">
              <div className="grid" style={{ gridTemplateColumns: `auto repeat(${column_names.length}, ${cellSize}px)` }}>
                {/* Top-left empty cell */}
                <div className="p-2"></div>
                
                {/* Column headers */}
                {column_names.map((name, i) => (
                  <motion.div
                    key={`header-${i}`}
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.05 }}
                    className="p-2 text-xs font-medium text-center"
                    style={{
                      writingMode: 'vertical-rl',
                      textOrientation: 'mixed',
                      height: `${cellSize * 2}px`
                    }}
                  >
                    <span className="truncate" title={name}>
                      {name.length > 15 ? name.substring(0, 12) + '...' : name}
                    </span>
                  </motion.div>
                ))}

                {/* Rows */}
                {correlation_matrix.map((row, i) => (
                  <>
                    {/* Row header */}
                    <motion.div
                      key={`row-header-${i}`}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="p-2 text-xs font-medium flex items-center justify-end pr-3"
                      style={{ maxWidth: '120px' }}
                    >
                      <span className="truncate" title={column_names[i]}>
                        {column_names[i].length > 15 ? column_names[i].substring(0, 12) + '...' : column_names[i]}
                      </span>
                    </motion.div>

                    {/* Cells */}
                    {row.map((value, j) => (
                      <motion.div
                        key={`cell-${i}-${j}`}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: (i + j) * 0.01 }}
                        className="border border-gray-200 dark:border-gray-700 flex items-center justify-center text-xs font-medium relative group cursor-pointer"
                        style={{
                          backgroundColor: getColorForValue(value),
                          color: Math.abs(value) > 0.5 ? 'white' : 'black',
                          width: `${cellSize}px`,
                          height: `${cellSize}px`
                        }}
                        title={`${column_names[i]} vs ${column_names[j]}: ${value.toFixed(3)}`}
                      >
                        {value.toFixed(2)}
                        
                        {/* Tooltip on hover */}
                        <div className="absolute bottom-full mb-2 hidden group-hover:block bg-gray-900 text-white text-xs rounded py-1 px-2 whitespace-nowrap z-10">
                          {column_names[i]} vs {column_names[j]}: {value.toFixed(3)}
                        </div>
                      </motion.div>
                    ))}
                  </>
                ))}
              </div>
            </div>
          </div>

          {/* Legend */}
          <div className="flex items-center justify-center gap-4 text-xs">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-red-500"></div>
              <span>Strong Negative</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-gray-300"></div>
              <span>Weak/None</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-blue-500"></div>
              <span>Strong Positive</span>
            </div>
          </div>

          {/* Strong Correlations List */}
          {strong_correlations && strong_correlations.length > 0 && (
            <div className="border-t pt-4">
              <h4 className="font-semibold text-sm mb-3">Strong Correlations (|r| &gt; 0.7)</h4>
              <div className="space-y-2">
                {strong_correlations.map((corr, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded"
                  >
                    <span className="text-sm">
                      <strong>{corr.param1}</strong> ↔ <strong>{corr.param2}</strong>
                    </span>
                    <span
                      className="font-mono text-sm px-2 py-1 rounded"
                      style={{
                        backgroundColor: getColorForValue(corr.coefficient),
                        color: Math.abs(corr.coefficient) > 0.5 ? 'white' : 'black'
                      }}
                    >
                      {corr.coefficient.toFixed(3)}
                    </span>
                  </motion.div>
                ))}
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
