import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Clock, Database, X } from 'lucide-react';
import { dataApi, HistoryItem } from '@/lib/api';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useDataStore } from '@/store/dataStore';
import { Button } from '@/components/ui/button';

export const HistoryList = () => {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const selectedDatasetId = useDataStore((state) => state.selectedDatasetId);

  useEffect(() => {
    loadHistory();
    
    // Listen for refresh events from file upload
    const handleRefresh = () => {
      loadHistory();
    };
    
    window.addEventListener('refresh-history', handleRefresh);
    
    return () => {
      window.removeEventListener('refresh-history', handleRefresh);
    };
  }, []);

  const loadHistory = async () => {
    try {
      const data = await dataApi.getHistory();
      setHistory(data);
    } catch (error) {
      console.error('Failed to load history:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectDataset = (id: number) => {
    useDataStore.getState().setSelectedDatasetId(id);
  };

  const handleClearSelection = () => {
    useDataStore.getState().setSelectedDatasetId(null);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-foreground flex items-center gap-2">
          <Clock className="w-4 h-4" />
          Recent Datasets
        </h3>
        {selectedDatasetId && (
          <Button
            variant="ghost"
            size="sm"
            onClick={handleClearSelection}
            className="h-6 px-2"
          >
            <X className="w-3 h-3" />
          </Button>
        )}
      </div>
      
      {history.length === 0 ? (
        <div className="text-center py-8 text-sm text-muted-foreground">
          No datasets yet. Upload a CSV to get started!
        </div>
      ) : (
        <ScrollArea className="h-[300px]">
          <div className="space-y-2 pr-4">
            {history.map((item, index) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                onClick={() => handleSelectDataset(item.id)}
                className={`p-3 rounded-lg cursor-pointer transition-all ${
                  selectedDatasetId === item.id
                    ? 'bg-primary/20 border-2 border-primary'
                    : 'bg-secondary hover:bg-secondary/80 border-2 border-transparent'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-medium text-foreground truncate max-w-[150px]" title={item.filename || `Dataset #${item.id}`}>
                    {item.filename || `Dataset #${item.id}`}
                  </span>
                  <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <Database className="w-3 h-3" />
                    <span>{item.total_records}</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <p className="text-xs text-muted-foreground">
                    {formatDate(item.uploaded_at)}
                  </p>
                  {item.status && (
                    <span className={`text-xs px-1.5 py-0.5 rounded ${
                      item.status === 'COMPLETED' ? 'bg-green-500/20 text-green-400' :
                      item.status === 'FAILED' ? 'bg-red-500/20 text-red-400' :
                      'bg-yellow-500/20 text-yellow-400'
                    }`}>
                      {item.status}
                    </span>
                  )}
                </div>
                {selectedDatasetId === item.id && (
                  <div className="text-xs text-primary font-medium mt-1">
                    ● Selected
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </ScrollArea>
      )}
    </div>
  );
};
