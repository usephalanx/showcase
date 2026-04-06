import React from "react";
import { TaskStatusFilter } from "../types/Task";

interface TaskFilterProps {
  current: TaskStatusFilter;
  onChange: (filter: TaskStatusFilter) => void;
}

const FILTERS: { label: string; value: TaskStatusFilter }[] = [
  { label: "All", value: "all" },
  { label: "Todo", value: "todo" },
  { label: "In Progress", value: "in-progress" },
  { label: "Done", value: "done" },
];

const TaskFilter: React.FC<TaskFilterProps> = ({ current, onChange }) => {
  return (
    <div style={{ display: "flex", gap: "8px", marginBottom: "16px" }}>
      {FILTERS.map((f) => (
        <button
          key={f.value}
          onClick={() => onChange(f.value)}
          style={{
            padding: "6px 14px",
            borderRadius: "4px",
            border: current === f.value ? "2px solid #4f46e5" : "1px solid #d1d5db",
            background: current === f.value ? "#eef2ff" : "#fff",
            color: current === f.value ? "#4f46e5" : "#374151",
            cursor: "pointer",
            fontWeight: current === f.value ? 600 : 400,
          }}
        >
          {f.label}
        </button>
      ))}
    </div>
  );
};

export default TaskFilter;
