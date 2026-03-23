import apiClient from './client';

/**
 * Authenticate a user with username and password.
 *
 * @param {string} username - The user's username.
 * @param {string} password - The user's password.
 * @returns {Promise<{access_token: string, token_type: string}>} The JWT token response.
 */
export async function loginUser(username, password) {
  const response = await apiClient.post('/auth/login', {
    username,
    password,
  });
  return response.data;
}

/**
 * Register a new user.
 *
 * @param {string} username - Desired username.
 * @param {string} password - Desired password.
 * @returns {Promise<{id: number, username: string, created_at: string}>} The created user.
 */
export async function registerUser(username, password) {
  const response = await apiClient.post('/auth/register', {
    username,
    password,
  });
  return response.data;
}
