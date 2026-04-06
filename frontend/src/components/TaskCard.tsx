import React from "react";
import StatusBadge from "./StatusBadge";

/**
 * Allowed status values for a task, matching the backend enum.
 */
export type TaskStatus = "todo" | "in-progress" | "done";

/**
 * Represents a single task entity as returned by the API.
 */
export interface Task {
  id: number;
  title: string;
  status: TaskStatus;
  due_date: string | null;
  created_at: string;
  updated_at: string;
}

export interface TaskCardProps {
  /** The task object to display. */
  task: Task;
  /** Callback invoked when the edit button is clicked. Receives the task. */
  onEdit: (task: Task) => void;
  /** Callback invoked when the delete button is clicked. Receives the task id. */
  onDelete: (taskId: number) => void;
  /** Callback invoked when the status should change. Receives the task id and new status. */
  onStatusChange: (taskId: number, newStatus: TaskStatus) => void;
}

/**
 * Format an ISO date string into a human-readable form.
 * Returns "No due date" when the value is null/undefined.
 */
function formatDueDate(dateStr: string | null): string {
  if (!dateStr) {
    return "No due date";
  }
  try {
    const date = new Date(dateStr + "T00:00:00");
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  } catch {
    return dateStr;
  }
}

/**
 * Determine the next logical status in the workflow.
 */
function getNextStatus(current: TaskStatus): TaskStatus {
  const flow: Record<TaskStatus, TaskStatus> = {
    todo: "in-progress",
    "in-progress": "done",
    done: "todo",
  };
  return flow[current];
}

/**
 * TaskCard displays a single task inside a styled card with action buttons.
 */
const TaskCard: React.FC<TaskCardProps> = ({
  task,
  onEdit,
  onDelete,
  onStatusChange,
}) => {
  const handleStatusClick = () => {
    onStatusChange(task.id, getNextStatus(task.status));
  };

  const handleEditClick = () => {
    onEdit(task);
  };

  const handleDeleteClick = () => {
    onDelete(task.id);
  };

  return (
    <div
      className="task-card"
      data-testid={`task-card-${task.id}`}
      style={{
        border: "1px solid #e2e8f0",
        borderRadius: "8px",
        padding: "16px",
        boxShadow: "0 1px 3px rgba(0, 0, 0, 0.08)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        gap: "12px",
        backgroundColor: "#ffffff",
        marginBottom: "8px",
      }}
    >
      {/* Left section: status badge + task info */}
      <div
        style={{ display: "flex", alignItems: "center", gap: "12px", flex: 1 }}
      >
        <button
          type="button"
          onClick={handleStatusClick}
          aria-label={`Change status of ${task.title}`}
          style={{ background: "none", border: "none", cursor: "pointer", padding: 0 }}
        >
          <StatusBadge status={task.status} />
        </button>

        <div style={{ flex: 1, minWidth: 0 }}>
          <h3
            style={{
              margin: 0,
              fontSize: "16px",
              fontWeight: 600,
              color: task.status === "done" ? "#94a3b8" : "#1e293b",
              textDecoration: task.status === "done" ? "line-through" : "none",
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
            }}
            data-testid="task-title"
          >
            {task.title}
          </h3>
          <span
            style={{ fontSize: "13px", color: "#64748b", marginTop: "2px", display: "block" }}
            data-testid="task-due-date"
          >
            {formatDueDate(task.due_date)}
          </span>
        </div>
      </div>

      {/* Right section: action buttons */}
      <div style={{ display: "flex", gap: "8px", flexShrink: 0 }}>
        <button
          type="button"
          onClick={handleEditClick}
          aria-label={`Edit ${task.title}`}
          data-testid="edit-button"
          style={{
            background: "none",
            border: "1px solid #e2e8f0",
            borderRadius: "6px",
            cursor: "pointer",
            padding: "6px 8px",
            fontSize: "16px",
            lineHeight: 1,
            color: "#475569",
          }}
        >
          ✏️
        </button>
        <button
          type="button"
          onClick={handleDeleteClick}
          aria-label={`Delete ${task.title}`}
          data-testid="delete-button"
          style={{
            background: "none",
            border: "1px solid #e2e8f0",
            borderRadius: "6px",
            cursor: "pointer",
            padding: "6px 8px",
            fontSize: "16px",
            lineHeight: 1,
            color: "#ef4444",
          }}
        >
          🗑️
        </button>
      </div>
    </div>
  );
};

export default TaskCard;
