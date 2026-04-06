import React, { useState, useEffect } from 'react';
import { Task, TaskStatus } from '../types/Task';

export interface TaskFormData {
  title: string;
  status: TaskStatus;
  due_date: string;
}

interface TaskFormProps {
  initial?: Task | null;
  onSubmit: (data: TaskFormData) => void;
  onCancel: () => void;
  loading?: boolean;
}

const TaskForm: React.FC<TaskFormProps> = ({ initial, onSubmit, onCancel, loading }) => {
  const [title, setTitle] = useState(initial?.title ?? '');
  const [status, setStatus] = useState<TaskStatus>(initial?.status ?? 'todo');
  const [dueDate, setDueDate] = useState(initial?.due_date ?? '');

  useEffect(() => {
    setTitle(initial?.title ?? '');
    setStatus(initial?.status ?? 'todo');
    setDueDate(initial?.due_date ?? '');
  }, [initial]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    onSubmit({ title: title.trim(), status, due_date: dueDate });
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <div>
        <label htmlFor="task-title" style={{ display: 'block', marginBottom: '4px', fontWeight: 600 }}>Title</label>
        <input
          id="task-title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
          maxLength={255}
          required
          style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #d1d5db', boxSizing: 'border-box' }}
        />
      </div>
      <div>
        <label htmlFor="task-status" style={{ display: 'block', marginBottom: '4px', fontWeight: 600 }}>Status</label>
        <select
          id="task-status"
          value={status}
          onChange={(e) => setStatus(e.target.value as TaskStatus)}
          style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #d1d5db', boxSizing: 'border-box' }}
        >
          <option value="todo">Todo</option>
          <option value="in-progress">In Progress</option>
          <option value="done">Done</option>
        </select>
      </div>
      <div>
        <label htmlFor="task-due-date" style={{ display: 'block', marginBottom: '4px', fontWeight: 600 }}>Due Date</label>
        <input
          id="task-due-date"
          type="date"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #d1d5db', boxSizing: 'border-box' }}
        />
      </div>
      <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
        <button
          type="button"
          onClick={onCancel}
          disabled={loading}
          style={{ padding: '8px 16px', borderRadius: '4px', border: '1px solid #d1d5db', background: '#fff', cursor: 'pointer' }}
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={loading || !title.trim()}
          style={{ padding: '8px 16px', borderRadius: '4px', border: 'none', background: '#2563eb', color: '#fff', cursor: 'pointer', opacity: loading ? 0.6 : 1 }}
        >
          {loading ? 'Saving…' : initial ? 'Update Task' : 'Add Task'}
        </button>
      </div>
    </form>
  );
};

export default TaskForm;
