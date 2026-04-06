import { Task } from "../types/Task";

const API_BASE = "http://localhost:8000/api/tasks";

export async function fetchTasks(status?: string): Promise<Task[]> {
  const url = status && status !== "all" ? `${API_BASE}?status=${status}` : API_BASE;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch tasks: ${res.status}`);
  return res.json();
}

export async function createTask(data: { title: string; status?: string; due_date?: string | null }): Promise<Task> {
  const res = await fetch(API_BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(`Failed to create task: ${res.status}`);
  return res.json();
}

export async function updateTask(
  id: number,
  data: { title?: string; status?: string; due_date?: string | null }
): Promise<Task> {
  const res = await fetch(`${API_BASE}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(`Failed to update task: ${res.status}`);
  return res.json();
}

export async function deleteTask(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error(`Failed to delete task: ${res.status}`);
}
