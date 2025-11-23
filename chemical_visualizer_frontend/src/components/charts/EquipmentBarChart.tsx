import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { DataSummary } from '@/store/dataStore';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface EquipmentBarChartProps {
  summary: DataSummary | null;
}

export const EquipmentBarChart = ({ summary }: EquipmentBarChartProps) => {
  const chartRef = useRef(null);

  useEffect(() => {
    // Trigger animation when data changes
    if (chartRef.current) {
      const chart = chartRef.current as any;
      chart.update('active');
    }
  }, [summary]);

  if (!summary) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-muted-foreground">No data available</p>
      </div>
    );
  }

  const data = {
    labels: Object.keys(summary.type_distribution),
    datasets: [
      {
        label: 'Equipment Count',
        data: Object.values(summary.type_distribution),
        backgroundColor: [
          'rgba(0, 188, 212, 0.8)',
          'rgba(255, 107, 53, 0.8)',
          'rgba(76, 175, 80, 0.8)',
          'rgba(156, 39, 176, 0.8)',
        ],
        borderColor: [
          'rgb(0, 188, 212)',
          'rgb(255, 107, 53)',
          'rgb(76, 175, 80)',
          'rgb(156, 39, 176)',
        ],
        borderWidth: 2,
        borderRadius: 8,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 1000,
      easing: 'easeInOutQuart' as const,
    },
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Equipment Type Distribution',
        color: 'hsl(210, 40%, 98%)',
        font: {
          size: 16,
          weight: 'bold' as const,
        },
      },
      tooltip: {
        backgroundColor: 'rgba(34, 40, 49, 0.95)',
        titleColor: 'hsl(210, 40%, 98%)',
        bodyColor: 'hsl(210, 40%, 98%)',
        borderColor: 'hsl(189, 94%, 43%)',
        borderWidth: 1,
        padding: 12,
        displayColors: true,
        callbacks: {
          label: function (context: any) {
            return `Count: ${context.parsed.y}`;
          },
        },
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
        ticks: {
          color: 'hsl(215, 20%, 65%)',
          font: {
            size: 12,
          },
        },
      },
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(255, 255, 255, 0.05)',
        },
        ticks: {
          color: 'hsl(215, 20%, 65%)',
          font: {
            size: 12,
          },
          precision: 0,
        },
      },
    },
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className="h-full"
    >
      <Bar ref={chartRef} data={data} options={options} />
    </motion.div>
  );
};
