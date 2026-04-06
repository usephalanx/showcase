/**
 * TaskCard component – renders a single task with action controls.
 *
 * This is a minimal implementation so that TaskList can import and
 * render it.  A more fully-featured version may be provided by a
 * dedicated task.
 */

import React from "react";
import type { Task, TaskStatus } from "./TaskList";

export interface TaskCardProps {
  /** The task object to display. */
  task: Task;
  /** Called when the user requests to edit this task. */
  onEdit: (task: Task) => void;
  /** Called when the user requests to delete this task. */
  onDelete: (taskId: number) => void;
  /** Called when the user changes the status of this task. */
  onStatusChange: (taskId: number, newStatus: TaskStatus) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({
  task,
  onEdit,
  onDelete,
  onStatusChange,
}) => {
  return (
    <div className="task-card" data-testid={`task-card-${task.id}`}>
      <h3 className="task-card__title">{task.title}</h3>
      <span className="task-card__status">{task.status}</span>
      {task.due_date && (
        <span className="task-card__due-date">{task.due_date}</span>
      )}
      <div className="task-card__actions">
        <button
          type="button"
          aria-label={`Edit ${task.title}`}
          onClick={() => onEdit(task)}
        >
          Edit
        </button>
        <button
          type="button"
          aria-label={`Delete ${task.title}`}
          onClick={() => onDelete(task.id)}
        >
          Delete
        </button>
        <select
          aria-label={`Change status of ${task.title}`}
          value={task.status}
          onChange={(e) =>
            onStatusChange(task.id, e.target.value as TaskStatus)
          }
        >
          <option value="todo">todo</option>
          <option value="in-progress">in-progress</option>
          <option value="done">done</option>
        </select>
      </div>
    </div>
  );
};

export default TaskCard;
