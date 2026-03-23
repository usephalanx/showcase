import apiClient from './client';

/**
 * Fetch tasks, optionally filtered by project ID.
 *
 * @param {number|string|null} projectId - Optional project ID filter.
 * @returns {Promise<Array>} List of task objects.
 */
export async function fetchTasks(projectId = null) {
  const params = projectId ? { project_id: projectId } : {};
  const response = await apiClient.get('/api/tasks', { params });
  return response.data;
}

/**
 * Fetch a single task by ID.
 *
 * @param {number|string} taskId - The task ID.
 * @returns {Promise<Object>} The task object.
 */
export async function fetchTask(taskId) {
  const response = await apiClient.get(`/api/tasks/${taskId}`);
  return response.data;
}

/**
 * Create a new task.
 *
 * @param {{project_id: number, title: string, status?: string, priority?: string, due_date?: string|null}} data
 * @returns {Promise<Object>} The created task.
 */
export async function createTask(data) {
  const response = await apiClient.post('/api/tasks', data);
  return response.data;
}

/**
 * Partially update a task.
 *
 * @param {number|string} taskId - The task ID.
 * @param {{title?: string, status?: string, priority?: string, due_date?: string|null}} data
 * @returns {Promise<Object>} The updated task.
 */
export async function updateTask(taskId, data) {
  const response = await apiClient.patch(`/api/tasks/${taskId}`, data);
  return response.data;
}

/**
 * Delete a task by ID.
 *
 * @param {number|string} taskId - The task ID.
 * @returns {Promise<Object>} Confirmation response.
 */
export async function deleteTask(taskId) {
  const response = await apiClient.delete(`/api/tasks/${taskId}`);
  return response.data;
}
