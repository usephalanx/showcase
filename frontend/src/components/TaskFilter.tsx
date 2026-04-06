/**
 * TaskFilter – a row of filter buttons/tabs for filtering tasks by status.
 *
 * Renders four buttons: All, Todo, In Progress, Done.
 * The currently active filter is visually highlighted.
 * Calls `onFilterChange` with the selected filter value when clicked.
 */

import React from "react";

export type TaskFilterStatus = "all" | "todo" | "in-progress" | "done";

export interface TaskFilterProps {
  /** The currently active filter value. */
  currentFilter: TaskFilterStatus;
  /** Callback invoked when the user selects a different filter. */
  onFilterChange: (filter: TaskFilterStatus) => void;
}

interface FilterOption {
  label: string;
  value: TaskFilterStatus;
}

const FILTER_OPTIONS: readonly FilterOption[] = [
  { label: "All", value: "all" },
  { label: "Todo", value: "todo" },
  { label: "In Progress", value: "in-progress" },
  { label: "Done", value: "done" },
] as const;

const TaskFilter: React.FC<TaskFilterProps> = ({
  currentFilter,
  onFilterChange,
}) => {
  return (
    <div
      role="tablist"
      aria-label="Filter tasks by status"
      style={{
        display: "flex",
        gap: "8px",
        flexWrap: "wrap",
      }}
    >
      {FILTER_OPTIONS.map(({ label, value }) => {
        const isActive = currentFilter === value;

        return (
          <button
            key={value}
            role="tab"
            type="button"
            aria-selected={isActive}
            aria-label={`Filter by ${label}`}
            onClick={() => onFilterChange(value)}
            style={{
              padding: "8px 16px",
              border: "1px solid #d1d5db",
              borderRadius: "6px",
              cursor: "pointer",
              fontWeight: isActive ? 700 : 400,
              backgroundColor: isActive ? "#3b82f6" : "#ffffff",
              color: isActive ? "#ffffff" : "#374151",
              transition: "background-color 0.15s, color 0.15s",
            }}
          >
            {label}
          </button>
        );
      })}
    </div>
  );
};

export default TaskFilter;
