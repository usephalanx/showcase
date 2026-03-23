import axios from 'axios';

/**
 * Pre-configured axios instance for communicating with the Kanban API.
 *
 * - baseURL is set to "/api" so Vite's dev proxy forwards to the backend.
 * - A request interceptor attaches the JWT from localStorage as a Bearer token.
 * - A response interceptor redirects to the login page on 401 responses.
 */
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: attach JWT token from localStorage
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: redirect to login on 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

/**
 * Register a new user account.
 *
 * @param {string} username - The desired username.
 * @param {string} email - The user's email address.
 * @param {string} password - The desired password.
 * @returns {Promise<import('axios').AxiosResponse>} The server response.
 */
export async function register(username, email, password) {
  const response = await api.post('/auth/register', { username, email, password });
  return response.data;
}

/**
 * Log in with existing credentials.
 *
 * @param {string} username - The user's username.
 * @param {string} password - The user's password.
 * @returns {Promise<import('axios').AxiosResponse>} The server response containing the JWT.
 */
export async function login(username, password) {
  const response = await api.post('/auth/login', { username, password });
  return response.data;
}

/**
 * Fetch all boards belonging to the authenticated user.
 *
 * @returns {Promise<Array>} A list of board objects.
 */
export async function getBoards() {
  const response = await api.get('/boards');
  return response.data;
}

/**
 * Create a new board.
 *
 * @param {string} title - The title of the new board.
 * @returns {Promise<Object>} The newly created board object.
 */
export async function createBoard(title) {
  const response = await api.post('/boards', { title });
  return response.data;
}

/**
 * Fetch a single board by ID, including its columns and cards.
 *
 * @param {number} id - The board's ID.
 * @returns {Promise<Object>} The board object with nested columns and cards.
 */
export async function getBoard(id) {
  const response = await api.get(`/boards/${id}`);
  return response.data;
}

/**
 * Delete a board by ID.
 *
 * @param {number} id - The board's ID.
 * @returns {Promise<Object>} The server confirmation response.
 */
export async function deleteBoard(id) {
  const response = await api.delete(`/boards/${id}`);
  return response.data;
}

/**
 * Create a new card in a column.
 *
 * @param {number} columnId - The target column's ID.
 * @param {string} title - The card title.
 * @param {string} description - The card description.
 * @returns {Promise<Object>} The newly created card object.
 */
export async function createCard(columnId, title, description) {
  const response = await api.post(`/columns/${columnId}/cards`, { title, description });
  return response.data;
}

/**
 * Update an existing card's fields.
 *
 * @param {number} id - The card's ID.
 * @param {Object} data - An object containing the fields to update.
 * @returns {Promise<Object>} The updated card object.
 */
export async function updateCard(id, data) {
  const response = await api.patch(`/cards/${id}`, data);
  return response.data;
}

/**
 * Delete a card by ID.
 *
 * @param {number} id - The card's ID.
 * @returns {Promise<Object>} The server confirmation response.
 */
export async function deleteCard(id) {
  const response = await api.delete(`/cards/${id}`);
  return response.data;
}

/**
 * Move a card to a different column and/or position.
 *
 * @param {number} id - The card's ID.
 * @param {number} targetColumnId - The target column's ID.
 * @param {number} targetPosition - The desired position index in the target column.
 * @returns {Promise<Object>} The updated card object.
 */
export async function moveCard(id, targetColumnId, targetPosition) {
  const response = await api.patch(`/cards/${id}/move`, {
    column_id: targetColumnId,
    position: targetPosition,
  });
  return response.data;
}

export default api;
