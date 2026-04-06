import React from "react";

/**
 * Represents a single filter option with its value and display label.
 */
interface FilterOption {
  value: string;
  label: string;
}

/**
 * Props for the TaskFilter component.
 */
export interface TaskFilterProps {
  /** The currently active filter value. */
  currentFilter: string;
  /** Callback invoked when the user selects a different filter. */
  onFilterChange: (filter: string) => void;
}

const FILTER_OPTIONS: FilterOption[] = [
  { value: "all", label: "All" },
  { value: "todo", label: "Todo" },
  { value: "in-progress", label: "In Progress" },
  { value: "done", label: "Done" },
];

/**
 * TaskFilter displays a row of buttons/tabs for filtering tasks by status.
 * The active filter is visually highlighted.
 */
const TaskFilter: React.FC<TaskFilterProps> = ({
  currentFilter,
  onFilterChange,
}) => {
  return (
    <div className="task-filter" role="group" aria-label="Filter tasks by status">
      {FILTER_OPTIONS.map((option) => {
        const isActive = currentFilter === option.value;

        return (
          <button
            key={option.value}
            type="button"
            className={`task-filter__button${
              isActive ? " task-filter__button--active" : ""
            }`}
            aria-pressed={isActive}
            onClick={() => onFilterChange(option.value)}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
};

export default TaskFilter;
