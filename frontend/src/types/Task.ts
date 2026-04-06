export interface Task {
  id: number;
  title: string;
  status: string;
  due_date: string | null;
}

export type TaskStatusFilter = "all" | "todo" | "in-progress" | "done";
