import React from "react";
import StatusBadge from "./StatusBadge";

/**
 * Allowed status values matching the backend TaskStatus enum.
 */
export type TaskStatus = "todo" | "in-progress" | "done";

/**
 * Task entity mirroring the backend TaskResponse schema.
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
  /** The task to display. */
  task: Task;
  /** Called when the user clicks the edit button. */
  onEdit: (task: Task) => void;
  /** Called when the user clicks the delete button. */
  onDelete: (task: Task) => void;
  /** Called when the user cycles the task status. Receives the next status. */
  onStatusChange: (task: Task, nextStatus: TaskStatus) => void;
}

const STATUS_CYCLE: Record<TaskStatus, TaskStatus> = {
  "todo": "in-progress",
  "in-progress": "done",
  "done": "todo",
};

const STATUS_CYCLE_LABELS: Record<TaskStatus, string> = {
  "todo": "Start",
  "in-progress": "Complete",
  "done": "Reopen",
};

/**
 * Format an ISO date string (YYYY-MM-DD) into a human-readable form.
 * Returns an em-dash when no date is provided.
 */
function formatDueDate(dueDate: string | null): string {
  if (!dueDate) {
    return "\u2014";
  }
  try {
    const date = new Date(dueDate + "T00:00:00");
    return date.toLocaleDateString(undefined, {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  } catch {
    return dueDate;
  }
}

const cardStyle: React.CSSProperties = {
  border: "1px solid #e2e8f0",
  borderRadius: "8px",
  padding: "16px",
  boxShadow: "0 1px 3px rgba(0, 0, 0, 0.08)",
  backgroundColor: "#ffffff",
  display: "flex",
  flexDirection: "column",
  gap: "12px",
};

const headerStyle: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "flex-start",
  gap: "8px",
};

const titleStyle: React.CSSProperties = {
  margin: 0,
  fontSize: "1.1rem",
  fontWeight: 600,
  color: "#1a202c",
  wordBreak: "break-word",
};

const dueDateStyle: React.CSSProperties = {
  fontSize: "0.85rem",
  color: "#718096",
  margin: 0,
};

const actionsStyle: React.CSSProperties = {
  display: "flex",
  gap: "8px",
  flexWrap: "wrap",
};

const buttonBase: React.CSSProperties = {
  padding: "6px 12px",
  borderRadius: "4px",
  border: "1px solid #cbd5e0",
  backgroundColor: "#f7fafc",
  cursor: "pointer",
  fontSize: "0.8rem",
  fontWeight: 500,
  lineHeight: 1.4,
};

/**
 * TaskCard displays a single task with its title, status badge,
 * formatted due date, and action buttons for edit, delete, and
 * status cycling.
 */
export default function TaskCard({
  task,
  onEdit,
  onDelete,
  onStatusChange,
}: TaskCardProps): React.ReactElement {
  const nextStatus = STATUS_CYCLE[task.status];
  const cycleLabel = STATUS_CYCLE_LABELS[task.status];

  return (
    <div style={cardStyle} data-testid={`task-card-${task.id}`}>
      <div style={headerStyle}>
        <h3 style={titleStyle}>{task.title}</h3>
        <StatusBadge status={task.status} />
      </div>

      <p style={dueDateStyle}>
        Due: {formatDueDate(task.due_date)}
      </p>

      <div style={actionsStyle}>
        <button
          type="button"
          style={{ ...buttonBase, borderColor: "#63b3ed", color: "#2b6cb0" }}
          aria-label={`Edit task: ${task.title}`}
          onClick={() => onEdit(task)}
        >
          Edit
        </button>
        <button
          type="button"
          style={{ ...buttonBase, borderColor: "#fc8181", color: "#c53030" }}
          aria-label={`Delete task: ${task.title}`}
          onClick={() => onDelete(task)}
        >
          Delete
        </button>
        <button
          type="button"
          style={{ ...buttonBase, borderColor: "#68d391", color: "#276749" }}
          aria-label={`${cycleLabel} task: ${task.title}`}
          onClick={() => onStatusChange(task, nextStatus)}
        >
          {cycleLabel}
        </button>
      </div>
    </div>
  );
}
