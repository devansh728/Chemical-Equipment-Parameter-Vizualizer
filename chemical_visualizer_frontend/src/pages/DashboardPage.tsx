import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { AnimatedBackground } from '@/components/decor/AnimatedBackground';
import { FosseeContent } from '@/components/dashboard/FosseeContent';
import { AnalysisView } from '@/components/dashboard/AnalysisView';
import { useDataStore } from '@/store/dataStore';
import { createWebSocket } from '@/lib/api';
import { toast } from 'sonner';
import { dataApi } from '@/lib/api';
import type { DatasetStats } from '@/store/dataStore';

export const DashboardPage = () => {
  const { summary, data, selectedDatasetId } = useDataStore();
  const [stats, setStats] = useState<DatasetStats | null>(null);

  // Fetch dataset details when a dataset is selected
  useEffect(() => {
    if (selectedDatasetId) {
      fetchDatasetDetail(selectedDatasetId);
    } else {
      // Clear summary and data when no selection
      useDataStore.getState().setSummary(null);
      useDataStore.getState().setData([]);
      setStats(null);
    }
  }, [selectedDatasetId]);

  const fetchDatasetDetail = async (id: number) => {
    try {
      useDataStore.getState().setLoading(true);
      const details = await dataApi.getDatasetDetail(id);
      useDataStore.getState().setSummary(details.summary);
      useDataStore.getState().setData(details.data || []);
      
      // Fetch stats separately
      try {
        const statsData = await dataApi.getDatasetStats(id);
        setStats(statsData);
      } catch (statsError) {
        console.error('Failed to fetch stats:', statsError);
        setStats(null);
      }
      
      toast.success('Dataset loaded successfully');
    } catch (error) {
      toast.error('Failed to load dataset details');
      // Clear selection on error
      useDataStore.getState().setSelectedDatasetId(null);
    } finally {
      useDataStore.getState().setLoading(false);
    }
  };

  // WebSocket for real-time updates (always connected)
  useEffect(() => {
    let ws: WebSocket | null = null;
    
    try {
      ws = createWebSocket();

      ws.onopen = () => {
        console.log('WebSocket connected');
        toast.success('Real-time updates connected');
      };

      ws.onmessage = (event: MessageEvent) => {
        const message = JSON.parse(event.data);
      
        // Handle multi-phase notifications
        if (message.status === 'profiling_complete') {
          toast.info('Phase 1/3: Column profiling complete', {
            description: 'AI suggestions generated'
          });
          // Refresh if viewing this dataset
          if (selectedDatasetId === message.dataset_id) {
            fetchDatasetDetail(message.dataset_id);
          }
        } else if (message.status === 'analysis_complete') {
          toast.info('Phase 2/3: Deep analysis complete', {
            description: `${message.outliers_count || 0} outliers detected`
          });
          // Refresh if viewing this dataset
          if (selectedDatasetId === message.dataset_id) {
            fetchDatasetDetail(message.dataset_id);
          }
        } else if (message.status === 'COMPLETED') {
          toast.success('Phase 3/3: Full analysis complete!', {
            description: 'AI insights are ready'
          });
          // Refresh the selected dataset if it matches
          if (selectedDatasetId === message.dataset_id) {
            fetchDatasetDetail(message.dataset_id);
          }
          // Note: We don't auto-select, user must click from history
        } else if (message.status === 'FAILED') {
          toast.error(`Analysis failed: ${message.error}`);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        toast.warning('Real-time updates unavailable');
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
      };
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      toast.warning('Real-time updates unavailable - will check status periodically');
    }

    return () => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [selectedDatasetId]);

  return (
    <>
      <AnimatedBackground />
      <DashboardLayout>
        <AnimatePresence mode="wait">
          {!selectedDatasetId ? (
            <motion.div
              key="fossee"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <FosseeContent />
            </motion.div>
          ) : (
            <motion.div
              key="analysis"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <AnalysisView summary={summary} data={data} stats={stats} />
            </motion.div>
          )}
        </AnimatePresence>
      </DashboardLayout>
    </>
  );
};
