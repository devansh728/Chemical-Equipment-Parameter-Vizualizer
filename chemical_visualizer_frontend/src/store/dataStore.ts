import { create } from 'zustand';

export interface EquipmentData {
  Equipment_ID: string;
  Type: string;
  Flowrate: number;
  Pressure: number;
  Temperature: number;
}

export interface DataSummary {
  dataset_id: number;
  uploaded_at: string;
  total_records: number;
  type_distribution: Record<string, number>;
  avg_temperature: number;
  avg_pressure: number;
  avg_flowrate?: number;
}

export interface DatasetStats {
  total_records: number;
  avg_pressure: number;
  avg_temperature: number;
  avg_flowrate: number;
}

interface DataState {
  summary: DataSummary | null;
  data: EquipmentData[];
  isLoading: boolean;
  datasetId: number | null;
  selectedDatasetId: number | null;
  setSummary: (summary: DataSummary) => void;
  setData: (data: EquipmentData[]) => void;
  setLoading: (loading: boolean) => void;
  setDatasetId: (id: number) => void;
  setSelectedDatasetId: (id: number | null) => void;
  reset: () => void;
}

export const useDataStore = create<DataState>((set) => ({
  summary: null,
  data: [],
  isLoading: false,
  datasetId: null,
  selectedDatasetId: null,
  setSummary: (summary) => set({ summary }),
  setData: (data) => set({ data }),
  setLoading: (isLoading) => set({ isLoading }),
  setDatasetId: (datasetId) => set({ datasetId }),
  setSelectedDatasetId: (selectedDatasetId) => set({ selectedDatasetId }),
  reset: () => set({ summary: null, data: [], datasetId: null, selectedDatasetId: null }),
}));
