import axios from 'axios';

/**
 * Pre-configured Axios instance for API communication.
 * In development, requests are proxied to the backend via Vite's dev server.
 * In production, requests go to the same origin.
 */
const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Response interceptor for consistent error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with a status outside 2xx
      console.error(
        `API Error: ${error.response.status} ${error.response.statusText}`,
        error.response.data,
      );
    } else if (error.request) {
      // Request was made but no response received
      console.error('API Error: No response received', error.request);
    } else {
      console.error('API Error:', error.message);
    }
    return Promise.reject(error);
  },
);

export default apiClient;
