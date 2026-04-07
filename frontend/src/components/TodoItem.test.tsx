import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import TodoItem, { Todo, TodoItemProps } from "./TodoItem";

const baseTodo: Todo = {
  id: "todo-1",
  text: "Buy groceries",
  completed: false,
  createdAt: Date.now(),
};

const renderTodoItem = (overrides: Partial<TodoItemProps> = {}) => {
  const defaultProps: TodoItemProps = {
    todo: baseTodo,
    onToggle: vi.fn(),
    onDelete: vi.fn(),
    ...overrides,
  };
  return { ...render(<TodoItem {...defaultProps} />), props: defaultProps };
};

describe("TodoItem", () => {
  it("renders todo text", () => {
    renderTodoItem();
    expect(screen.getByText("Buy groceries")).toBeInTheDocument();
  });

  it("checkbox reflects completed state when false", () => {
    renderTodoItem();
    const checkbox = screen.getByRole("checkbox") as HTMLInputElement;
    expect(checkbox.checked).toBe(false);
  });

  it("checkbox reflects completed state when true", () => {
    const completedTodo: Todo = { ...baseTodo, completed: true };
    renderTodoItem({ todo: completedTodo });
    const checkbox = screen.getByRole("checkbox") as HTMLInputElement;
    expect(checkbox.checked).toBe(true);
  });

  it("calls onToggle with todo id when checkbox is clicked", () => {
    const onToggle = vi.fn();
    renderTodoItem({ onToggle });
    fireEvent.click(screen.getByRole("checkbox"));
    expect(onToggle).toHaveBeenCalledTimes(1);
    expect(onToggle).toHaveBeenCalledWith("todo-1");
  });

  it("calls onDelete with todo id when delete button is clicked", () => {
    const onDelete = vi.fn();
    renderTodoItem({ onDelete });
    fireEvent.click(screen.getByRole("button", { name: /delete/i }));
    expect(onDelete).toHaveBeenCalledTimes(1);
    expect(onDelete).toHaveBeenCalledWith("todo-1");
  });

  it("completed todo has line-through text decoration", () => {
    const completedTodo: Todo = { ...baseTodo, completed: true };
    renderTodoItem({ todo: completedTodo });
    const textEl = screen.getByTestId("todo-text");
    expect(textEl.style.textDecoration).toBe("line-through");
  });

  it("incomplete todo has no line-through text decoration", () => {
    renderTodoItem();
    const textEl = screen.getByTestId("todo-text");
    expect(textEl.style.textDecoration).toBe("none");
  });
});
