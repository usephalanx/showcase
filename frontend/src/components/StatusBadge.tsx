import React from 'react';
import { TaskStatus } from '../types/Task';

interface StatusBadgeProps {
  status: TaskStatus;
  onClick?: () => void;
}

const STATUS_COLORS: Record<TaskStatus, string> = {
  'todo': '#6b7280',
  'in-progress': '#2563eb',
  'done': '#16a34a',
};

const STATUS_LABELS: Record<TaskStatus, string> = {
  'todo': 'Todo',
  'in-progress': 'In Progress',
  'done': 'Done',
};

const StatusBadge: React.FC<StatusBadgeProps> = ({ status, onClick }) => {
  return (
    <span
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') onClick?.(); }}
      style={{
        display: 'inline-block',
        padding: '4px 12px',
        borderRadius: '12px',
        fontSize: '0.75rem',
        fontWeight: 600,
        color: '#fff',
        backgroundColor: STATUS_COLORS[status],
        cursor: onClick ? 'pointer' : 'default',
        userSelect: 'none',
      }}
      title={onClick ? 'Click to cycle status' : undefined}
    >
      {STATUS_LABELS[status]}
    </span>
  );
};

export default StatusBadge;
