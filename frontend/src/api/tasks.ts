/**
 * API service module for Task CRUD operations.
 *
 * Uses an axios instance configured with a base URL sourced from the
 * `VITE_API_BASE_URL` environment variable. When the variable is not
 * set the instance falls back to an empty string, which means requests
 * are sent to the same origin (useful with Vite's dev-server proxy).
 */

import axios, { type AxiosInstance, type AxiosResponse } from "axios";

import type { Task, TaskCreate, TaskUpdate } from "../types";

/** Base URL resolved from environment or defaulting to same-origin. */
const BASE_URL: string = import.meta.env.VITE_API_BASE_URL ?? "";

/**
 * Pre-configured axios instance for all task-related HTTP requests.
 *
 * - `baseURL` points to the API root.
 * - JSON `Content-Type` header is set by default.
 * - Timeout is set to 15 seconds.
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 15_000,
});

/**
 * Fetch all tasks from the API.
 *
 * @returns A promise resolving to the array of tasks.
 */
export async function getTasks(): Promise<Task[]> {
  const response: AxiosResponse<Task[]> = await apiClient.get<Task[]>(
    "/api/tasks",
  );
  return response.data;
}

/**
 * Create a new task.
 *
 * @param data - The task creation payload.
 * @returns A promise resolving to the newly created task.
 */
export async function createTask(data: TaskCreate): Promise<Task> {
  const response: AxiosResponse<Task> = await apiClient.post<Task>(
    "/api/tasks",
    data,
  );
  return response.data;
}

/**
 * Update an existing task by its ID.
 *
 * Uses PATCH semantics — only the supplied fields are modified.
 *
 * @param id   - The ID of the task to update.
 * @param data - An object containing the fields to update.
 * @returns A promise resolving to the updated task.
 */
export async function updateTask(id: number, data: TaskUpdate): Promise<Task> {
  const response: AxiosResponse<Task> = await apiClient.patch<Task>(
    `/api/tasks/${id}`,
    data,
  );
  return response.data;
}

/**
 * Delete a task by its ID.
 *
 * @param id - The ID of the task to delete.
 * @returns A promise that resolves when the deletion is complete.
 */
export async function deleteTask(id: number): Promise<void> {
  await apiClient.delete(`/api/tasks/${id}`);
}

export { apiClient };
