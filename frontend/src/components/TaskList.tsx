import React from 'react';
import { Task } from '../types/Task';
import StatusBadge from './StatusBadge';

interface TaskListProps {
  tasks: Task[];
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
  onStatusCycle: (task: Task) => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onEdit, onDelete, onStatusCycle }) => {
  if (tasks.length === 0) {
    return <p style={{ textAlign: 'center', color: '#6b7280', padding: '32px 0' }}>No tasks yet. Add one!</p>;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      {tasks.map((task) => (
        <div
          key={task.id}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '12px 16px',
            border: '1px solid #e5e7eb',
            borderRadius: '8px',
            background: '#fff',
          }}
        >
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontWeight: 600, fontSize: '1rem', marginBottom: '4px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {task.title}
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem', color: '#6b7280' }}>
              <StatusBadge status={task.status} onClick={() => onStatusCycle(task)} />
              {task.due_date && <span>Due: {task.due_date}</span>}
            </div>
          </div>
          <div style={{ display: 'flex', gap: '8px', marginLeft: '12px', flexShrink: 0 }}>
            <button
              onClick={() => onEdit(task)}
              style={{ padding: '6px 12px', borderRadius: '4px', border: '1px solid #d1d5db', background: '#fff', cursor: 'pointer', fontSize: '0.85rem' }}
            >
              Edit
            </button>
            <button
              onClick={() => onDelete(task)}
              style={{ padding: '6px 12px', borderRadius: '4px', border: '1px solid #ef4444', background: '#fff', color: '#ef4444', cursor: 'pointer', fontSize: '0.85rem' }}
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default TaskList;
