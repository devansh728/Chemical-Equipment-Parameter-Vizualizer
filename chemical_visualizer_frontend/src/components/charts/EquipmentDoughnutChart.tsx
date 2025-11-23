import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';
import { Doughnut } from 'react-chartjs-2';
import { DataSummary } from '@/store/dataStore';

ChartJS.register(ArcElement, Tooltip, Legend);

interface EquipmentDoughnutChartProps {
  summary: DataSummary | null;
}

export const EquipmentDoughnutChart = ({ summary }: EquipmentDoughnutChartProps) => {
  const chartRef = useRef(null);

  useEffect(() => {
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
        label: 'Equipment Distribution',
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
        hoverOffset: 10,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      animateRotate: true,
      animateScale: true,
      duration: 1000,
      easing: 'easeInOutQuart' as const,
    },
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          color: 'hsl(215, 20%, 65%)',
          padding: 15,
          font: {
            size: 12,
          },
          usePointStyle: true,
          pointStyle: 'circle',
        },
      },
      title: {
        display: true,
        text: 'Equipment Type Proportion',
        color: 'hsl(210, 40%, 98%)',
        font: {
          size: 16,
          weight: 'bold' as const,
        },
        padding: {
          top: 10,
          bottom: 20,
        },
      },
      tooltip: {
        backgroundColor: 'rgba(34, 40, 49, 0.95)',
        titleColor: 'hsl(210, 40%, 98%)',
        bodyColor: 'hsl(210, 40%, 98%)',
        borderColor: 'hsl(189, 94%, 43%)',
        borderWidth: 1,
        padding: 12,
        callbacks: {
          label: function (context: any) {
            const label = context.label || '';
            const value = context.parsed || 0;
            const total = context.dataset.data.reduce((acc: number, val: number) => acc + val, 0);
            const percentage = ((value / total) * 100).toFixed(1);
            return `${label}: ${value} (${percentage}%)`;
          },
        },
      },
    },
    cutout: '65%',
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, ease: 'easeOut', delay: 0.1 }}
      className="h-full flex items-center justify-center"
    >
      <Doughnut ref={chartRef} data={data} options={options} />
    </motion.div>
  );
};
