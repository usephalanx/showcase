import React, { useState, useEffect, useCallback } from "react";
import { Task, TaskStatusFilter } from "./types/Task";
import { fetchTasks, createTask, updateTask, deleteTask } from "./api/taskApi";
import TaskFilter from "./components/TaskFilter";
import TaskForm from "./components/TaskForm";
import TaskItem from "./components/TaskItem";

const App: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filter, setFilter] = useState<TaskStatusFilter>("all");
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadTasks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchTasks(filter);
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  }, [filter]);

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  const handleSubmit = async (data: { title: string; status: string; due_date: string | null }) => {
    setError(null);
    try {
      if (editingTask) {
        await updateTask(editingTask.id, data);
        setEditingTask(null);
      } else {
        await createTask(data);
      }
      await loadTasks();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Operation failed");
    }
  };

  const handleDelete = async (id: number) => {
    setError(null);
    try {
      await deleteTask(id);
      if (editingTask?.id === id) setEditingTask(null);
      await loadTasks();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Delete failed");
    }
  };

  const handleStatusChange = async (id: number, status: string) => {
    setError(null);
    try {
      await updateTask(id, { status });
      await loadTasks();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Status update failed");
    }
  };

  const handleEdit = (task: Task) => {
    setEditingTask(task);
  };

  const handleCancelEdit = () => {
    setEditingTask(null);
  };

  return (
    <div style={{ maxWidth: "680px", margin: "0 auto", padding: "32px 16px", fontFamily: "system-ui, -apple-system, sans-serif" }}>
      <h1 style={{ fontSize: "28px", fontWeight: 700, marginBottom: "24px", color: "#111827" }}>Todo App</h1>

      <TaskForm editingTask={editingTask} onSubmit={handleSubmit} onCancel={handleCancelEdit} />

      <TaskFilter current={filter} onChange={setFilter} />

      {error && (
        <div style={{ padding: "10px 14px", marginBottom: "12px", borderRadius: "6px", background: "#fef2f2", color: "#dc2626", border: "1px solid #fca5a5", fontSize: "14px" }}>
          {error}
        </div>
      )}

      {loading ? (
        <p style={{ color: "#6b7280", textAlign: "center", padding: "24px 0" }}>Loading tasks…</p>
      ) : tasks.length === 0 ? (
        <p style={{ color: "#6b7280", textAlign: "center", padding: "24px 0" }}>
          No tasks found.{filter !== "all" ? " Try a different filter." : " Add one above!"}
        </p>
      ) : (
        <div>
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onEdit={handleEdit}
              onDelete={handleDelete}
              onStatusChange={handleStatusChange}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default App;
