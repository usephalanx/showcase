export type TaskStatus = 'todo' | 'in-progress' | 'done';

export interface Task {
  id: number;
  title: string;
  status: TaskStatus;
  due_date: string | null;
  created_at: string;
  updated_at: string;
}

export interface TaskCreatePayload {
  title: string;
  status?: TaskStatus;
  due_date?: string | null;
}

export interface TaskUpdatePayload {
  title?: string;
  status?: TaskStatus;
  due_date?: string | null;
}
