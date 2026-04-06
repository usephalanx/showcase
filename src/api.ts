/**
 * Frontend API service for the Todo application.
 *
 * Provides an axios instance configured with the backend base URL and
 * typed helper functions for all CRUD operations on tasks.
 */

import axios, { type AxiosInstance, type AxiosResponse } from "axios";

/**
 * Allowed status values for a task, matching the backend TaskStatus enum.
 */
export type TaskStatus = "todo" | "in-progress" | "done";

/**
 * Shape of a task as returned by the API.
 */
export interface Task {
  id: number;
  title: string;
  status: TaskStatus;
  due_date: string | null;
}

/**
 * Payload accepted when creating a new task.
 */
export interface TaskCreateData {
  title: string;
  status?: TaskStatus;
  due_date?: string | null;
}

/**
 * Payload accepted when updating an existing task.
 * All fields are optional to support partial updates.
 */
export interface TaskUpdateData {
  title?: string;
  status?: TaskStatus;
  due_date?: string | null;
}

/**
 * Determine the API base URL.
 *
 * In production the frontend is served from the same origin so we use
 * the "/api" prefix.  During local development (Vite dev-server on
 * port 5173) we point at the FastAPI backend on port 8000.
 */
function resolveBaseURL(): string {
  if (typeof window !== "undefined" && window.location.port === "5173") {
    return "http://localhost:8000/api";
  }
  return "/api";
}

/**
 * Pre-configured axios instance targeting the Todo backend.
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: resolveBaseURL(),
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10_000,
});

/**
 * Fetch all tasks, optionally filtered by status.
 *
 * @param status - When provided, only tasks with this status are returned.
 * @returns A promise resolving to an array of Task objects.
 */
export async function getTasks(status?: TaskStatus): Promise<Task[]> {
  const params: Record<string, string> = {};
  if (status !== undefined) {
    params.status = status;
  }
  const response: AxiosResponse<Task[]> = await apiClient.get("/tasks", {
    params,
  });
  return response.data;
}

/**
 * Create a new task.
 *
 * @param data - The fields for the new task (title is required).
 * @returns A promise resolving to the newly created Task.
 */
export async function createTask(data: TaskCreateData): Promise<Task> {
  const response: AxiosResponse<Task> = await apiClient.post("/tasks", data);
  return response.data;
}

/**
 * Update an existing task by id.
 *
 * @param id   - The primary-key id of the task to update.
 * @param data - An object containing only the fields to change.
 * @returns A promise resolving to the updated Task.
 */
export async function updateTask(
  id: number,
  data: TaskUpdateData,
): Promise<Task> {
  const response: AxiosResponse<Task> = await apiClient.put(
    `/tasks/${id}`,
    data,
  );
  return response.data;
}

/**
 * Delete a task by id.
 *
 * @param id - The primary-key id of the task to remove.
 * @returns A promise resolving to the response payload (confirmation).
 */
export async function deleteTask(
  id: number,
): Promise<{ detail: string }> {
  const response: AxiosResponse<{ detail: string }> = await apiClient.delete(
    `/tasks/${id}`,
  );
  return response.data;
}

export default apiClient;
