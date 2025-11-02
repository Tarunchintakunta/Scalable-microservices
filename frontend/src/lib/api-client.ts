/**
 * API Client with Axios
 */
import axios, { AxiosInstance, AxiosError } from 'axios';
import { API_CONFIG } from '../config/api';

// Create axios instances for each service
export const serviceA = axios.create({
  baseURL: API_CONFIG.SERVICE_A_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const serviceB = axios.create({
  baseURL: API_CONFIG.SERVICE_B_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
const addAuthInterceptor = (instance: AxiosInstance) => {
  instance.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );
};

// Response interceptor for error handling
const addErrorInterceptor = (instance: AxiosInstance) => {
  instance.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
      if (error.response?.status === 401) {
        // Unauthorized - clear token and redirect to login
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
      return Promise.reject(error);
    }
  );
};

// Apply interceptors
addAuthInterceptor(serviceA);
addAuthInterceptor(serviceB);
addErrorInterceptor(serviceA);
addErrorInterceptor(serviceB);

export default { serviceA, serviceB };
