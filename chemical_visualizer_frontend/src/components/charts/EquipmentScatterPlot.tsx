import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js';
import { Scatter } from 'react-chartjs-2';
import { EquipmentData } from '@/store/dataStore';

ChartJS.register(LinearScale, PointElement, LineElement, Tooltip, Legend);

interface EquipmentScatterPlotProps {
  data: EquipmentData[];
}

export const EquipmentScatterPlot = ({ data }: EquipmentScatterPlotProps) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (chartRef.current) {
      const chart = chartRef.current as any;
      chart.update('active');
    }
  }, [data]);

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-muted-foreground">No data available</p>
      </div>
    );
  }

  // Normalize temperature for color mapping
  const temps = data.map((d) => d.Temperature);
  const minTemp = Math.min(...temps);
  const maxTemp = Math.max(...temps);

  const getColorByTemperature = (temp: number) => {
    const normalized = (temp - minTemp) / (maxTemp - minTemp);
    if (normalized < 0.33) return 'rgba(0, 188, 212, 0.8)'; // Cool
    if (normalized < 0.66) return 'rgba(76, 175, 80, 0.8)'; // Medium
    return 'rgba(255, 107, 53, 0.8)'; // Hot
  };

  const scatterData = {
    datasets: [
      {
        label: 'Flowrate vs Pressure',
        data: data.map((item) => ({
          x: item.Flowrate,
          y: item.Pressure,
          temperature: item.Temperature,
          type: item.Type,
        })),
        backgroundColor: data.map((item) => getColorByTemperature(item.Temperature)),
        borderColor: data.map((item) => getColorByTemperature(item.Temperature).replace('0.8', '1')),
        borderWidth: 2,
        pointRadius: 6,
        pointHoverRadius: 8,
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
        display: true,
        position: 'top' as const,
        labels: {
          color: 'hsl(215, 20%, 65%)',
          font: {
            size: 12,
          },
        },
      },
      title: {
        display: true,
        text: 'Flowrate vs Pressure (Color = Temperature)',
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
        callbacks: {
          label: function (context: any) {
            const point = context.raw;
            return [
              `Type: ${point.type}`,
              `Flowrate: ${point.x.toFixed(1)}`,
              `Pressure: ${point.y.toFixed(1)}`,
              `Temperature: ${point.temperature.toFixed(1)}°F`,
            ];
          },
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Flowrate',
          color: 'hsl(210, 40%, 98%)',
          font: {
            size: 14,
            weight: 'bold' as const,
          },
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.05)',
        },
        ticks: {
          color: 'hsl(215, 20%, 65%)',
          font: {
            size: 12,
          },
        },
      },
      y: {
        title: {
          display: true,
          text: 'Pressure',
          color: 'hsl(210, 40%, 98%)',
          font: {
            size: 14,
            weight: 'bold' as const,
          },
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.05)',
        },
        ticks: {
          color: 'hsl(215, 20%, 65%)',
          font: {
            size: 12,
          },
        },
      },
    },
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut', delay: 0.2 }}
      className="h-full"
    >
      <Scatter ref={chartRef} data={scatterData} options={options} />
    </motion.div>
  );
};
