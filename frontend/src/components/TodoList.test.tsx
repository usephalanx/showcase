import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import TodoList, { Todo, TodoListProps } from './TodoList';

const makeTodo = (overrides: Partial<Todo> = {}): Todo => ({
  id: 'todo-1',
  text: 'Buy groceries',
  completed: false,
  createdAt: Date.now(),
  ...overrides,
});

const renderTodoList = (props: Partial<TodoListProps> = {}) => {
  const defaultProps: TodoListProps = {
    todos: [],
    onToggle: vi.fn(),
    onDelete: vi.fn(),
    ...props,
  };
  return { ...render(<TodoList {...defaultProps} />), props: defaultProps };
};

describe('TodoList', () => {
  it('renders without crashing', () => {
    renderTodoList();
  });

  it('shows empty message when todos array is empty', () => {
    renderTodoList({ todos: [] });
    expect(screen.getByTestId('empty-message')).toBeInTheDocument();
    expect(screen.getByText('No todos yet!')).toBeInTheDocument();
  });

  it('does not show empty message when todos exist', () => {
    renderTodoList({ todos: [makeTodo()] });
    expect(screen.queryByTestId('empty-message')).not.toBeInTheDocument();
  });

  it('renders the correct number of todo items', () => {
    const todos: Todo[] = [
      makeTodo({ id: '1', text: 'First' }),
      makeTodo({ id: '2', text: 'Second' }),
      makeTodo({ id: '3', text: 'Third' }),
    ];
    renderTodoList({ todos });
    expect(screen.getByTestId('todo-item-1')).toBeInTheDocument();
    expect(screen.getByTestId('todo-item-2')).toBeInTheDocument();
    expect(screen.getByTestId('todo-item-3')).toBeInTheDocument();
  });

  it('renders todo text for each item', () => {
    const todos: Todo[] = [
      makeTodo({ id: '1', text: 'Buy milk' }),
      makeTodo({ id: '2', text: 'Walk the dog' }),
    ];
    renderTodoList({ todos });
    expect(screen.getByText('Buy milk')).toBeInTheDocument();
    expect(screen.getByText('Walk the dog')).toBeInTheDocument();
  });

  it('calls onToggle with the correct id when checkbox is clicked', () => {
    const onToggle = vi.fn();
    const todos: Todo[] = [makeTodo({ id: 'abc-123', text: 'Test todo' })];
    renderTodoList({ todos, onToggle });

    fireEvent.click(screen.getByTestId('todo-toggle-abc-123'));
    expect(onToggle).toHaveBeenCalledTimes(1);
    expect(onToggle).toHaveBeenCalledWith('abc-123');
  });

  it('calls onDelete with the correct id when delete button is clicked', () => {
    const onDelete = vi.fn();
    const todos: Todo[] = [makeTodo({ id: 'def-456', text: 'Delete me' })];
    renderTodoList({ todos, onDelete });

    fireEvent.click(screen.getByTestId('todo-delete-def-456'));
    expect(onDelete).toHaveBeenCalledTimes(1);
    expect(onDelete).toHaveBeenCalledWith('def-456');
  });

  it('renders completed todos with a checked checkbox', () => {
    const todos: Todo[] = [makeTodo({ id: '1', text: 'Done', completed: true })];
    renderTodoList({ todos });
    const checkbox = screen.getByTestId('todo-toggle-1') as HTMLInputElement;
    expect(checkbox.checked).toBe(true);
  });

  it('renders incomplete todos with an unchecked checkbox', () => {
    const todos: Todo[] = [makeTodo({ id: '1', text: 'Not done', completed: false })];
    renderTodoList({ todos });
    const checkbox = screen.getByTestId('todo-toggle-1') as HTMLInputElement;
    expect(checkbox.checked).toBe(false);
  });
});
