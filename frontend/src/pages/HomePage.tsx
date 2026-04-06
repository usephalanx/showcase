import React, { useState, useEffect, useCallback } from 'react';
import { Task, TaskStatus } from '../types/Task';
import { getTasks, createTask, updateTask, deleteTask } from '../api/taskService';
import TaskList from '../components/TaskList';
import TaskForm, { TaskFormData } from '../components/TaskForm';

const NEXT_STATUS: Record<TaskStatus, TaskStatus> = {
  'todo': 'in-progress',
  'in-progress': 'done',
  'done': 'todo',
};

const HomePage: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getTasks();
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleAdd = () => {
    setEditingTask(null);
    setShowForm(true);
  };

  const handleEdit = (task: Task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  const handleSubmit = async (data: TaskFormData) => {
    try {
      setSaving(true);
      setError(null);
      if (editingTask) {
        const updated = await updateTask(editingTask.id, {
          title: data.title,
          status: data.status,
          due_date: data.due_date || null,
        });
        setTasks((prev) => prev.map((t) => (t.id === updated.id ? updated : t)));
      } else {
        const created = await createTask({
          title: data.title,
          status: data.status,
          due_date: data.due_date || null,
        });
        setTasks((prev) => [created, ...prev]);
      }
      setShowForm(false);
      setEditingTask(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save task');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (task: Task) => {
    const confirmed = window.confirm(`Delete "${task.title}"?`);
    if (!confirmed) return;
    try {
      setError(null);
      await deleteTask(task.id);
      setTasks((prev) => prev.filter((t) => t.id !== task.id));
      if (editingTask?.id === task.id) {
        setShowForm(false);
        setEditingTask(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task');
    }
  };

  const handleStatusCycle = async (task: Task) => {
    const nextStatus = NEXT_STATUS[task.status];
    try {
      setError(null);
      const updated = await updateTask(task.id, { status: nextStatus });
      setTasks((prev) => prev.map((t) => (t.id === updated.id ? updated : t)));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update status');
    }
  };

  return (
    <div style={{ maxWidth: '720px', margin: '0 auto', padding: '24px 16px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '1.5rem' }}>Todo App</h1>
        <button
          onClick={handleAdd}
          style={{
            padding: '8px 20px',
            borderRadius: '6px',
            border: 'none',
            background: '#2563eb',
            color: '#fff',
            fontWeight: 600,
            cursor: 'pointer',
            fontSize: '0.9rem',
          }}
        >
          + Add Task
        </button>
      </div>

      {error && (
        <div
          style={{
            padding: '12px 16px',
            marginBottom: '16px',
            borderRadius: '6px',
            background: '#fef2f2',
            border: '1px solid #fecaca',
            color: '#dc2626',
            fontSize: '0.9rem',
          }}
        >
          {error}
        </div>
      )}

      {showForm && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0,0,0,0.4)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
          }}
          onClick={(e) => { if (e.target === e.currentTarget) handleCancel(); }}
        >
          <div
            style={{
              background: '#fff',
              borderRadius: '12px',
              padding: '24px',
              width: '100%',
              maxWidth: '480px',
              boxShadow: '0 20px 60px rgba(0,0,0,0.2)',
            }}
          >
            <h2 style={{ margin: '0 0 16px', fontSize: '1.2rem' }}>
              {editingTask ? 'Edit Task' : 'New Task'}
            </h2>
            <TaskForm
              initial={editingTask}
              onSubmit={handleSubmit}
              onCancel={handleCancel}
              loading={saving}
            />
          </div>
        </div>
      )}

      {loading ? (
        <p style={{ textAlign: 'center', color: '#6b7280', padding: '32px 0' }}>Loading tasks…</p>
      ) : (
        <TaskList
          tasks={tasks}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onStatusCycle={handleStatusCycle}
        />
      )}
    </div>
  );
};

export default HomePage;
