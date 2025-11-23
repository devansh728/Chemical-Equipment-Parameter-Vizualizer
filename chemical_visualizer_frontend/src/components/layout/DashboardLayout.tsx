import { ReactNode } from 'react';
import { motion } from 'framer-motion';
import { Sidebar } from './Sidebar';
import { Button } from '@/components/ui/button';
import { LogOut, Download } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import { useDataStore } from '@/store/dataStore';
import { dataApi } from '@/lib/api';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

interface DashboardLayoutProps {
  children: ReactNode;
}

export const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  const logout = useAuthStore((state) => state.logout);
  const selectedDatasetId = useDataStore((state) => state.selectedDatasetId);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
    toast.success('Logged out successfully');
  };

  const handleDownloadReport = async () => {
    if (!selectedDatasetId) {
      toast.error('No dataset selected for download');
      return;
    }
    
    try {
      await dataApi.downloadReport(selectedDatasetId);
      toast.success('Report downloaded successfully');
    } catch (error) {
      toast.error('Failed to download report');
    }
  };

  const headerTitle = selectedDatasetId 
    ? `Dataset #${selectedDatasetId} Analysis`
    : 'FOSSEE Chemical Equipment Visualizer';

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <motion.header
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className="h-16 border-b border-border bg-card px-6 flex items-center justify-between"
        >
          <h1 className="text-xl font-bold text-foreground">{headerTitle}</h1>
          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="sm"
              onClick={handleDownloadReport}
              disabled={!selectedDatasetId}
              className="gap-2"
            >
              <Download className="w-4 h-4" />
              Download Report
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleLogout}
              className="gap-2"
            >
              <LogOut className="w-4 h-4" />
              Logout
            </Button>
          </div>
        </motion.header>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
};
