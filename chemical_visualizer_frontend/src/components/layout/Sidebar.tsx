import { motion } from 'framer-motion';
import { FileUpload } from './FileUpload';
import { HistoryList } from './HistoryList';
import { Separator } from '@/components/ui/separator';
import { FlaskConical } from 'lucide-react';

export const Sidebar = () => {
  return (
    <motion.aside
      initial={{ x: -300, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className="w-80 bg-card border-r border-border p-6 space-y-6 overflow-y-auto"
    >
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
          <FlaskConical className="w-5 h-5 text-primary" />
        </div>
        <div>
          <h2 className="text-lg font-bold text-foreground">Equipment</h2>
          <p className="text-xs text-muted-foreground">Parameter Visualizer</p>
        </div>
      </div>

      <Separator />

      <FileUpload />

      <Separator />

      <HistoryList />
    </motion.aside>
  );
};
