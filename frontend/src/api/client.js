import axios from 'axios';

/**
 * Base URL for the API.
 * In development, Vite proxy handles forwarding.
 * In production, set VITE_API_BASE_URL environment variable.
 */
const BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

/**
 * Axios instance pre-configured with the API base URL.
 * Includes a request interceptor that attaches the JWT access token
 * from localStorage to every outgoing request's Authorization header.
 */
const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: attach JWT token if available
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Response interceptor: redirect to login on 401
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear stored token and redirect to login
      localStorage.removeItem('access_token');
      // Only redirect if not already on the login page
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  },
);

export default apiClient;
