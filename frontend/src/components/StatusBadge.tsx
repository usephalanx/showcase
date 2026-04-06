import React from "react";

export type TaskStatus = "todo" | "in-progress" | "done";

export interface StatusBadgeProps {
  /** The current task status to display. */
  status: TaskStatus;
}

const STATUS_LABELS: Record<TaskStatus, string> = {
  "todo": "Todo",
  "in-progress": "In Progress",
  "done": "Done",
};

const STATUS_COLORS: Record<TaskStatus, { bg: string; text: string }> = {
  "todo": { bg: "#ebf8ff", text: "#2b6cb0" },
  "in-progress": { bg: "#fefcbf", text: "#975a16" },
  "done": { bg: "#f0fff4", text: "#276749" },
};

/**
 * StatusBadge renders a small coloured pill indicating the current
 * status of a task.
 */
export default function StatusBadge({ status }: StatusBadgeProps): React.ReactElement {
  const colors = STATUS_COLORS[status] ?? { bg: "#edf2f7", text: "#4a5568" };

  const style: React.CSSProperties = {
    display: "inline-block",
    padding: "2px 10px",
    borderRadius: "9999px",
    fontSize: "0.75rem",
    fontWeight: 600,
    backgroundColor: colors.bg,
    color: colors.text,
    whiteSpace: "nowrap",
  };

  return (
    <span style={style} data-testid="status-badge">
      {STATUS_LABELS[status] ?? status}
    </span>
  );
}
