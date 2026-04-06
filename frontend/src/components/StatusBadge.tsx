import React from "react";

/**
 * The set of valid task statuses.
 */
export type TaskStatus = "todo" | "in-progress" | "done";

/**
 * Props for the StatusBadge component.
 */
export interface StatusBadgeProps {
  /** Current status of the task. */
  status: TaskStatus;
  /** Optional click handler invoked when the badge is clicked. */
  onClick?: (status: TaskStatus) => void;
}

const STATUS_CONFIG: Record<
  TaskStatus,
  { label: string; backgroundColor: string; color: string }
> = {
  todo: {
    label: "Todo",
    backgroundColor: "#e2e8f0",
    color: "#475569",
  },
  "in-progress": {
    label: "In Progress",
    backgroundColor: "#dbeafe",
    color: "#1d4ed8",
  },
  done: {
    label: "Done",
    backgroundColor: "#dcfce7",
    color: "#16a34a",
  },
};

const baseStyle: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  padding: "4px 12px",
  borderRadius: "9999px",
  fontSize: "0.75rem",
  fontWeight: 600,
  lineHeight: 1.5,
  letterSpacing: "0.025em",
  border: "none",
  whiteSpace: "nowrap",
  userSelect: "none",
  transition: "opacity 0.15s ease-in-out",
};

/**
 * StatusBadge displays a task's status as a colored pill / badge.
 *
 * Colours:
 * - `todo`        → gray
 * - `in-progress` → blue
 * - `done`        → green
 *
 * When an `onClick` handler is provided the badge renders as a `<button>`
 * (for accessibility); otherwise it renders as a `<span>`.
 */
const StatusBadge: React.FC<StatusBadgeProps> = ({ status, onClick }) => {
  const config = STATUS_CONFIG[status];

  const style: React.CSSProperties = {
    ...baseStyle,
    backgroundColor: config.backgroundColor,
    color: config.color,
    cursor: onClick ? "pointer" : "default",
  };

  if (onClick) {
    return (
      <button
        type="button"
        data-testid="status-badge"
        data-status={status}
        style={style}
        onClick={() => onClick(status)}
        aria-label={`Status: ${config.label}`}
      >
        {config.label}
      </button>
    );
  }

  return (
    <span
      data-testid="status-badge"
      data-status={status}
      style={style}
      aria-label={`Status: ${config.label}`}
    >
      {config.label}
    </span>
  );
};

export default StatusBadge;
