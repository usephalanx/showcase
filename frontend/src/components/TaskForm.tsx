import React, { useState, useEffect } from "react";
import { Task } from "../types/Task";

interface TaskFormProps {
  editingTask: Task | null;
  onSubmit: (data: { title: string; status: string; due_date: string | null }) => void;
  onCancel: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ editingTask, onSubmit, onCancel }) => {
  const [title, setTitle] = useState("");
  const [status, setStatus] = useState("todo");
  const [dueDate, setDueDate] = useState("");

  useEffect(() => {
    if (editingTask) {
      setTitle(editingTask.title);
      setStatus(editingTask.status);
      setDueDate(editingTask.due_date ?? "");
    } else {
      setTitle("");
      setStatus("todo");
      setDueDate("");
    }
  }, [editingTask]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    onSubmit({ title: title.trim(), status, due_date: dueDate || null });
    if (!editingTask) {
      setTitle("");
      setStatus("todo");
      setDueDate("");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "24px", padding: "16px", border: "1px solid #e5e7eb", borderRadius: "8px", background: "#f9fafb" }}>
      <h3 style={{ margin: "0 0 12px" }}>{editingTask ? "Edit Task" : "New Task"}</h3>
      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        <input
          type="text"
          placeholder="Task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          style={{ padding: "8px 12px", borderRadius: "4px", border: "1px solid #d1d5db", fontSize: "14px" }}
        />
        <div style={{ display: "flex", gap: "10px" }}>
          <select value={status} onChange={(e) => setStatus(e.target.value)} style={{ padding: "8px 12px", borderRadius: "4px", border: "1px solid #d1d5db", fontSize: "14px" }}>
            <option value="todo">Todo</option>
            <option value="in-progress">In Progress</option>
            <option value="done">Done</option>
          </select>
          <input
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            style={{ padding: "8px 12px", borderRadius: "4px", border: "1px solid #d1d5db", fontSize: "14px" }}
          />
        </div>
        <div style={{ display: "flex", gap: "8px" }}>
          <button type="submit" style={{ padding: "8px 20px", borderRadius: "4px", border: "none", background: "#4f46e5", color: "#fff", cursor: "pointer", fontWeight: 600 }}>
            {editingTask ? "Update" : "Add Task"}
          </button>
          {editingTask && (
            <button type="button" onClick={onCancel} style={{ padding: "8px 20px", borderRadius: "4px", border: "1px solid #d1d5db", background: "#fff", cursor: "pointer" }}>
              Cancel
            </button>
          )}
        </div>
      </div>
    </form>
  );
};

export default TaskForm;
