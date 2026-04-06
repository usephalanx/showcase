/**
 * StatusBadge — displays a task status as a colored pill/badge.
 *
 * Colors:
 *   - todo        → gray
 *   - in-progress → blue
 *   - done        → green
 */

import React from "react";

export type StatusType = "todo" | "in-progress" | "done";

export interface StatusBadgeProps {
  /** Current task status. */
  status: StatusType;
}

const STATUS_CONFIG: Record<
  StatusType,
  { label: string; backgroundColor: string; color: string }
> = {
  todo: {
    label: "Todo",
    backgroundColor: "#e2e2e2",
    color: "#555555",
  },
  "in-progress": {
    label: "In Progress",
    backgroundColor: "#dbeafe",
    color: "#1d4ed8",
  },
  done: {
    label: "Done",
    backgroundColor: "#d1fae5",
    color: "#065f46",
  },
};

const baseStyle: React.CSSProperties = {
  display: "inline-block",
  padding: "2px 10px",
  borderRadius: "9999px",
  fontSize: "0.75rem",
  fontWeight: 600,
  lineHeight: "1.25rem",
  whiteSpace: "nowrap",
  textTransform: "capitalize",
};

export default function StatusBadge({ status }: StatusBadgeProps): React.ReactElement {
  const config = STATUS_CONFIG[status];

  const style: React.CSSProperties = {
    ...baseStyle,
    backgroundColor: config.backgroundColor,
    color: config.color,
  };

  return (
    <span data-testid="status-badge" data-status={status} style={style}>
      {config.label}
    </span>
  );
}
