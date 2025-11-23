import { motion } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Activity, TrendingUp, Thermometer, ArrowLeft, Sparkles, Brain, Network, AlertTriangle, Zap } from 'lucide-react';
import { EquipmentBarChart } from '@/components/charts/EquipmentBarChart';
import { EquipmentDoughnutChart } from '@/components/charts/EquipmentDoughnutChart';
import { EquipmentScatterPlot } from '@/components/charts/EquipmentScatterPlot';
import { AIInsightsCard } from '@/components/ai/AIInsightsCard';
import { SmartSuggestions } from '@/components/ai/SmartSuggestions';
import { CorrelationHeatmap } from '@/components/ai/CorrelationHeatmap';
import { OutlierExplorer } from '@/components/ai/OutlierExplorer';
import { OptimizationPanel } from '@/components/ai/OptimizationPanel';
import { StatisticalSummary } from '@/components/dashboard/StatisticalSummary';
import { DataSummary, EquipmentData, DatasetStats } from '@/store/dataStore';
import { useDataStore } from '@/store/dataStore';
import { useState, useEffect } from 'react';
import { dataApi } from '@/lib/api';

interface AnalysisViewProps {
  summary: DataSummary | null;
  data: EquipmentData[];
  stats: DatasetStats | null;
}

export const AnalysisView = ({ summary, data, stats }: AnalysisViewProps) => {
  const { selectedDatasetId } = useDataStore();
  const [datasetDetails, setDatasetDetails] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Fetch full dataset details for AI features
  useEffect(() => {
    const fetchDatasetDetails = async () => {
      if (!selectedDatasetId) return;
      
      setLoading(true);
      try {
        const details = await dataApi.getDatasetDetail(selectedDatasetId);
        setDatasetDetails(details);
      } catch (error) {
        console.error('Failed to fetch dataset details:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDatasetDetails();
  }, [selectedDatasetId]);

  const clearSelection = () => {
    useDataStore.getState().setSelectedDatasetId(null);
  };

  return (
    <div className="space-y-6">
      {/* Back Button */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.3 }}
      >
        <Button
          variant="ghost"
          onClick={clearSelection}
          className="gap-2"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Overview
        </Button>
      </motion.div>

      {/* Stats Cards */}
      {stats && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-4"
        >
          <Card className="bg-card/80 backdrop-blur-sm border-border/50">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Records</CardTitle>
              <Activity className="h-4 w-4 text-primary" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">{stats.total_records || 0}</div>
              <p className="text-xs text-muted-foreground mt-1">
                Equipment entries analyzed
              </p>
            </CardContent>
          </Card>

          <Card className="bg-card/80 backdrop-blur-sm border-border/50">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avg Pressure</CardTitle>
              <TrendingUp className="h-4 w-4 text-accent" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">
                {stats.avg_pressure?.toFixed(1) || '0.0'} PSI
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                Across all equipment
              </p>
            </CardContent>
          </Card>

          <Card className="bg-card/80 backdrop-blur-sm border-border/50">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avg Temperature</CardTitle>
              <Thermometer className="h-4 w-4 text-accent" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">
                {stats.avg_temperature?.toFixed(1) || '0.0'}°F
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                Operating temperature
              </p>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Charts Grid */}
      <Tabs defaultValue="overview" className="w-full">
        <TabsList className="grid w-full grid-cols-5 mb-6">
          <TabsTrigger value="overview" className="gap-2">
            <Activity className="h-4 w-4" />
            Overview
          </TabsTrigger>
          <TabsTrigger value="ai-insights" className="gap-2">
            <Sparkles className="h-4 w-4" />
            AI Insights
          </TabsTrigger>
          <TabsTrigger value="correlations" className="gap-2">
            <Network className="h-4 w-4" />
            Correlations
          </TabsTrigger>
          <TabsTrigger value="outliers" className="gap-2">
            <AlertTriangle className="h-4 w-4" />
            Outliers
          </TabsTrigger>
          <TabsTrigger value="optimization" className="gap-2">
            <Zap className="h-4 w-4" />
            Optimization
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab - Original Charts */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 }}
            >
              <Card className="bg-card/80 backdrop-blur-sm border-border/50 h-[400px]">
                <CardHeader>
                  <CardTitle>Type Distribution</CardTitle>
                  <CardDescription>Equipment count by type</CardDescription>
                </CardHeader>
                <CardContent className="h-[300px]">
                  <EquipmentBarChart summary={summary} />
                </CardContent>
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
            >
              <Card className="bg-card/80 backdrop-blur-sm border-border/50 h-[400px]">
                <CardHeader>
                  <CardTitle>Equipment Proportion</CardTitle>
                  <CardDescription>Percentage breakdown by type</CardDescription>
                </CardHeader>
                <CardContent className="h-[300px]">
                  <EquipmentDoughnutChart summary={summary} />
                </CardContent>
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3 }}
              className="lg:col-span-2"
            >
              <Card className="bg-card/80 backdrop-blur-sm border-border/50 h-[500px]">
                <CardHeader>
                  <CardTitle>Parameter Correlation</CardTitle>
                  <CardDescription>
                    Flowrate vs Pressure analysis (colored by temperature)
                  </CardDescription>
                </CardHeader>
                <CardContent className="h-[400px]">
                  <EquipmentScatterPlot data={data} />
                </CardContent>
              </Card>
            </motion.div>

            {/* Statistical Summary */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.4 }}
              className="lg:col-span-2"
            >
              <StatisticalSummary enhancedSummary={datasetDetails?.enhanced_summary || null} />
            </motion.div>
          </div>
        </TabsContent>

        {/* AI Insights Tab */}
        <TabsContent value="ai-insights" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <AIInsightsCard 
              aiInsights={datasetDetails?.ai_insights || null}
              loading={loading || !datasetDetails?.ai_complete}
            />
            <SmartSuggestions 
              suggestions={datasetDetails?.ai_suggestions || null}
              loading={loading || !datasetDetails?.profiling_complete}
            />
          </div>
        </TabsContent>

        {/* Correlations Tab */}
        <TabsContent value="correlations">
          <CorrelationHeatmap 
            correlationData={datasetDetails?.correlation_matrix || null}
            loading={loading || !datasetDetails?.analysis_complete}
          />
        </TabsContent>

        {/* Outliers Tab */}
        <TabsContent value="outliers">
          <OutlierExplorer 
            outliers={datasetDetails?.outliers || null}
            datasetId={selectedDatasetId || 0}
            loading={loading || !datasetDetails?.analysis_complete}
          />
        </TabsContent>

        {/* Optimization Tab */}
        <TabsContent value="optimization">
          <OptimizationPanel 
            datasetId={selectedDatasetId || 0}
            analysisComplete={datasetDetails?.analysis_complete || false}
          />
        </TabsContent>
      </Tabs>
    </div>
  );
};
