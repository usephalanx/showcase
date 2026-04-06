/**
 * TaskList component – renders a list of TaskCard components.
 *
 * Displays an empty-state message when the tasks array is empty.
 * Forwards onEdit, onDelete, and onStatusChange callbacks to each
 * TaskCard instance.
 */

import React from "react";
import TaskCard from "./TaskCard";

/**
 * Allowed status values – mirrors the backend TaskStatus enum.
 */
export type TaskStatus = "todo" | "in-progress" | "done";

/**
 * Shape of a single task object expected by the list.
 */
export interface Task {
  id: number;
  title: string;
  status: TaskStatus;
  due_date: string | null;
  created_at: string;
  updated_at: string;
}

export interface TaskListProps {
  /** Array of task objects to render. */
  tasks: Task[];
  /** Message displayed when the tasks array is empty. */
  emptyMessage?: string;
  /** Called when the user requests to edit a task. */
  onEdit: (task: Task) => void;
  /** Called when the user requests to delete a task. */
  onDelete: (taskId: number) => void;
  /** Called when the user changes the status of a task. */
  onStatusChange: (taskId: number, newStatus: TaskStatus) => void;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  emptyMessage = "No tasks yet. Create one to get started!",
  onEdit,
  onDelete,
  onStatusChange,
}) => {
  if (tasks.length === 0) {
    return (
      <div className="task-list task-list--empty" role="status">
        <p className="task-list__empty-message">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <ul className="task-list" role="list">
      {tasks.map((task) => (
        <li key={task.id} className="task-list__item">
          <TaskCard
            task={task}
            onEdit={onEdit}
            onDelete={onDelete}
            onStatusChange={onStatusChange}
          />
        </li>
      ))}
    </ul>
  );
};

export default TaskList;
