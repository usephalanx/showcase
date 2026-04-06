import React from "react";
import { Task } from "../types/Task";

interface TaskItemProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
  onStatusChange: (id: number, status: string) => void;
}

const STATUS_COLORS: Record<string, string> = {
  todo: "#f59e0b",
  "in-progress": "#3b82f6",
  done: "#10b981",
};

const TaskItem: React.FC<TaskItemProps> = ({ task, onEdit, onDelete, onStatusChange }) => {
  const nextStatus = task.status === "todo" ? "in-progress" : task.status === "in-progress" ? "done" : "todo";

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "12px 16px",
        border: "1px solid #e5e7eb",
        borderRadius: "8px",
        marginBottom: "8px",
        background: task.status === "done" ? "#f0fdf4" : "#fff",
      }}
    >
      <div style={{ flex: 1 }}>
        <span
          style={{
            fontWeight: 600,
            textDecoration: task.status === "done" ? "line-through" : "none",
            color: task.status === "done" ? "#6b7280" : "#111827",
          }}
        >
          {task.title}
        </span>
        <div style={{ display: "flex", gap: "8px", marginTop: "4px", alignItems: "center" }}>
          <span
            style={{
              fontSize: "12px",
              padding: "2px 8px",
              borderRadius: "12px",
              background: STATUS_COLORS[task.status] ?? "#6b7280",
              color: "#fff",
            }}
          >
            {task.status}
          </span>
          {task.due_date && (
            <span style={{ fontSize: "12px", color: "#6b7280" }}>Due: {task.due_date}</span>
          )}
        </div>
      </div>
      <div style={{ display: "flex", gap: "6px" }}>
        <button
          onClick={() => onStatusChange(task.id, nextStatus)}
          title={`Move to ${nextStatus}`}
          style={{ padding: "4px 10px", borderRadius: "4px", border: "1px solid #d1d5db", background: "#fff", cursor: "pointer", fontSize: "12px" }}
        >
          → {nextStatus}
        </button>
        <button
          onClick={() => onEdit(task)}
          style={{ padding: "4px 10px", borderRadius: "4px", border: "1px solid #d1d5db", background: "#fff", cursor: "pointer", fontSize: "12px" }}
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(task.id)}
          style={{ padding: "4px 10px", borderRadius: "4px", border: "1px solid #fca5a5", background: "#fef2f2", color: "#dc2626", cursor: "pointer", fontSize: "12px" }}
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskItem;
