/**
 * API client functions for project CRUD operations.
 */

import type { Project, ProjectCreatePayload } from '../types';

const API_BASE = '/api/projects';

/**
 * Fetch all projects from the backend.
 */
export async function fetchProjects(): Promise<Project[]> {
  const response = await fetch(API_BASE);
  if (!response.ok) {
    throw new Error(`Failed to fetch projects: ${response.status}`);
  }
  return response.json();
}

/**
 * Create a new project.
 */
export async function createProject(payload: ProjectCreatePayload): Promise<Project> {
  const response = await fetch(API_BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || `Failed to create project: ${response.status}`);
  }
  return response.json();
}

/**
 * Delete a project by ID.
 */
export async function deleteProject(id: number): Promise<void> {
  const response = await fetch(`${API_BASE}/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || `Failed to delete project: ${response.status}`);
  }
}
