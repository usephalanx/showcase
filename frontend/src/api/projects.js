import apiClient from './client';

/**
 * Fetch all projects.
 *
 * @returns {Promise<Array>} List of project objects.
 */
export async function fetchProjects() {
  const response = await apiClient.get('/api/projects');
  return response.data;
}

/**
 * Fetch a single project by ID.
 *
 * @param {number|string} projectId - The project ID.
 * @returns {Promise<Object>} The project object.
 */
export async function fetchProject(projectId) {
  const response = await apiClient.get(`/api/projects/${projectId}`);
  return response.data;
}

/**
 * Create a new project.
 *
 * @param {{name: string, description?: string}} data - Project creation data.
 * @returns {Promise<Object>} The created project.
 */
export async function createProject(data) {
  const response = await apiClient.post('/api/projects', data);
  return response.data;
}

/**
 * Delete a project by ID.
 *
 * @param {number|string} projectId - The project ID.
 * @returns {Promise<Object>} Confirmation response.
 */
export async function deleteProject(projectId) {
  const response = await apiClient.delete(`/api/projects/${projectId}`);
  return response.data;
}
