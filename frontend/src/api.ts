/**
 * Axios-based API service for the Todo application.
 *
 * Provides typed functions for every CRUD operation exposed by the
 * FastAPI backend.  The base URL defaults to http://localhost:8000 so
 * the Vite dev-server can proxy-free reach the backend during local
 * development.
 */

import axios from 'axios';
import type { Task, TaskCreate, TaskUpdate } from './types';

/** Pre-configured Axios instance pointing at the backend. */
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetch every task.
 *
 * @returns A promise that resolves to an array of tasks.
 */
export async function getTasks(): Promise<Task[]> {
  const response = await api.get<Task[]>('/tasks');
  return response.data;
}

/**
 * Fetch a single task by its id.
 *
 * @param id - The unique identifier of the task.
 * @returns A promise that resolves to the requested task.
 */
export async function getTask(id: number): Promise<Task> {
  const response = await api.get<Task>(`/tasks/${id}`);
  return response.data;
}

/**
 * Create a new task.
 *
 * @param data - The fields for the new task.
 * @returns A promise that resolves to the newly created task.
 */
export async function createTask(data: TaskCreate): Promise<Task> {
  const response = await api.post<Task>('/tasks', data);
  return response.data;
}

/**
 * Update an existing task.
 *
 * @param id   - The unique identifier of the task to update.
 * @param data - The fields to change.
 * @returns A promise that resolves to the updated task.
 */
export async function updateTask(id: number, data: TaskUpdate): Promise<Task> {
  const response = await api.put<Task>(`/tasks/${id}`, data);
  return response.data;
}

/**
 * Delete a task.
 *
 * @param id - The unique identifier of the task to delete.
 * @returns A promise that resolves when the deletion is complete.
 */
export async function deleteTask(id: number): Promise<void> {
  await api.delete(`/tasks/${id}`);
}

export default api;
