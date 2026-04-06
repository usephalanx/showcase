import React from "react";
import StatusBadge from "./StatusBadge";

export interface Task {
  id: number;
  title: string;
  status: string;
  due_date: string | null;
}

export interface TaskItemProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onStatusChange: (taskId: number, newStatus: string) => void;
}

const STATUS_OPTIONS: { value: string; label: string }[] = [
  { value: "todo", label: "Todo" },
  { value: "in-progress", label: "In Progress" },
  { value: "done", label: "Done" },
];

function formatDueDate(dateStr: string | null): string {
  if (!dateStr) {
    return "No due date";
  }
  try {
    const date = new Date(dateStr + "T00:00:00");
    if (isNaN(date.getTime())) {
      return "Invalid date";
    }
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  } catch {
    return "Invalid date";
  }
}

const TaskItem: React.FC<TaskItemProps> = ({
  task,
  onEdit,
  onDelete,
  onStatusChange,
}) => {
  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onStatusChange(task.id, e.target.value);
  };

  const handleEdit = () => {
    onEdit(task);
  };

  const handleDelete = () => {
    onDelete(task.id);
  };

  return (
    <div
      className="task-item"
      data-testid={`task-item-${task.id}`}
      style={{
        display: "flex",
        alignItems: "center",
        gap: "12px",
        padding: "12px 16px",
        borderBottom: "1px solid #e5e7eb",
      }}
    >
      <div
        className="task-item-content"
        style={{ flex: 1, minWidth: 0 }}
      >
        <span
          className="task-item-title"
          data-testid="task-title"
          style={{
            fontWeight: 500,
            fontSize: "1rem",
            display: "block",
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          }}
        >
          {task.title}
        </span>
        <span
          className="task-item-due-date"
          data-testid="task-due-date"
          style={{
            fontSize: "0.85rem",
            color: "#6b7280",
            display: "block",
            marginTop: "2px",
          }}
        >
          {formatDueDate(task.due_date)}
        </span>
      </div>

      <StatusBadge status={task.status} />

      <select
        className="task-item-status-select"
        data-testid="task-status-select"
        value={task.status}
        onChange={handleStatusChange}
        aria-label="Change task status"
        style={{
          padding: "4px 8px",
          borderRadius: "4px",
          border: "1px solid #d1d5db",
          fontSize: "0.85rem",
        }}
      >
        {STATUS_OPTIONS.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>

      <button
        className="task-item-edit-btn"
        data-testid="task-edit-btn"
        onClick={handleEdit}
        aria-label="Edit task"
        style={{
          padding: "6px 12px",
          borderRadius: "4px",
          border: "1px solid #d1d5db",
          background: "#f9fafb",
          cursor: "pointer",
          fontSize: "0.85rem",
        }}
      >
        Edit
      </button>

      <button
        className="task-item-delete-btn"
        data-testid="task-delete-btn"
        onClick={handleDelete}
        aria-label="Delete task"
        style={{
          padding: "6px 12px",
          borderRadius: "4px",
          border: "1px solid #fca5a5",
          background: "#fef2f2",
          color: "#dc2626",
          cursor: "pointer",
          fontSize: "0.85rem",
        }}
      >
        Delete
      </button>
    </div>
  );
};

export default TaskItem;
