import axios from 'axios';
import { useAuthStore } from '@/store/authStore';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling and token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = useAuthStore.getState().refreshToken;
      if (refreshToken) {
        try {
          const response = await api.post('/api/token/refresh/', { 
            refresh: refreshToken 
          });
          const newToken = response.data.access;
          useAuthStore.getState().updateToken(newToken);
          
          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return api(originalRequest);
        } catch (refreshError) {
          useAuthStore.getState().logout();
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      } else {
        useAuthStore.getState().logout();
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export const authApi = {

  // authApi.login to store both tokens
  login: async (username: string, password: string) => {
    const response = await api.post('/api/token/', { username, password });
    return { 
      access: response.data.access,
      refresh: response.data.refresh 
    };
  },

  signup: async (username: string, email: string, password: string) => {
    const response = await api.post('/api/signup/', { username, email, password });
    return {
      access: response.data.access,
      refresh: response.data.refresh,
    };
  },
  // Add refresh token method
  refreshToken: async (refresh: string) => {
    const response = await api.post('/api/token/refresh/', { refresh });
    return response.data.access;
 }
};

export interface HistoryItem {
  id: number;
  uploaded_at: string;
  total_records: number;
  filename: string;
  status: string;
}

export const dataApi = {
  uploadCSV: async (file: File, onProgress?: (progress: number) => void) => {
    const formData = new FormData();
    formData.append('file', file);
  
    const response = await api.post('/api/upload/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress?.(progress);
        }
      },
    });
  
    return response.data;
  },

  getHistory: async (): Promise<HistoryItem[]> => {
    const response = await api.get('/api/history/');
    return response.data.map((item: any) => ({
      id: item.id,
      uploaded_at: item.uploaded_at,
      total_records: item.summary?.total_records || 0,
      filename: item.filename,
      status: item.status
    }));
  },

  getDatasetDetail: async (datasetId: number) => {
    const response = await api.get(`/api/dataset/${datasetId}/`);
    return response.data;
  },

  downloadReport: async (datasetId: number) => {
    const response = await api.get(`/api/dataset/${datasetId}/report/`, {
      responseType: 'blob',
    });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `report_${datasetId}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },

  // AI Enhancement Endpoints
  explainOutlier: async (datasetId: number, outlierData: {
    equipment_name: string;
    equipment_type: string;
    parameter: string;
    value: number;
    expected_range: [number, number];
  }) => {
    const response = await api.post(`/api/dataset/${datasetId}/explain-outlier/`, outlierData);
    return response.data;
  },

  getOptimizations: async (datasetId: number) => {
    const response = await api.get(`/api/dataset/${datasetId}/optimize/`);
    return response.data;
  },

  getCorrelationData: async (datasetId: number) => {
    const response = await api.get(`/api/dataset/${datasetId}/correlation/`);
    return response.data;
  },

  getDatasetStats: async (datasetId: number) => {
    const response = await api.get(`/api/dataset/${datasetId}/stats/`);
    return response.data;
  }
};

// WebSocket connection
export const createWebSocket = (): WebSocket => {
  const token = localStorage.getItem('access_token');
  const wsUrl = `ws://localhost:8000/ws/analysis/?token=${token}`;
  console.log('Creating WebSocket with URL:', wsUrl);
  console.log('Token:', token ? 'present' : 'missing');
  return new WebSocket(wsUrl);
};


