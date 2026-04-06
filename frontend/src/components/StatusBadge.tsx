import React from "react";

/**
 * The set of valid task statuses that the badge can display.
 */
export type TaskStatus = "todo" | "in-progress" | "done";

/**
 * Props for the {@link StatusBadge} component.
 */
export interface StatusBadgeProps {
  /** The current status of the task. */
  status: TaskStatus;
}

/**
 * Mapping from each status value to its display label.
 */
const STATUS_LABELS: Record<TaskStatus, string> = {
  todo: "Todo",
  "in-progress": "In Progress",
  done: "Done",
};

/**
 * Mapping from each status value to its background + text color styles.
 */
const STATUS_STYLES: Record<TaskStatus, React.CSSProperties> = {
  todo: {
    backgroundColor: "#e2e8f0",
    color: "#334155",
  },
  "in-progress": {
    backgroundColor: "#fef3c7",
    color: "#92400e",
  },
  done: {
    backgroundColor: "#d1fae5",
    color: "#065f46",
  },
};

/**
 * Base styles shared by every badge variant.
 */
const BASE_STYLE: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  padding: "2px 10px",
  borderRadius: "9999px",
  fontSize: "0.75rem",
  fontWeight: 600,
  lineHeight: "1.25rem",
  whiteSpace: "nowrap",
  userSelect: "none",
};

/**
 * Displays a task's status as a colored pill / badge.
 *
 * Renders a small, rounded badge whose background color and label
 * correspond to the given {@link TaskStatus} value:
 *
 * - **todo** – grey/slate
 * - **in-progress** – amber/yellow
 * - **done** – green
 */
const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const colorStyle = STATUS_STYLES[status];
  const label = STATUS_LABELS[status];

  return (
    <span
      data-testid="status-badge"
      data-status={status}
      style={{ ...BASE_STYLE, ...colorStyle }}
    >
      {label}
    </span>
  );
};

export default StatusBadge;
