/**
 * Tests for the pure todo helper utilities.
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import {
  generateId,
  createTodo,
  toggleTodo,
  filterTodos,
} from '../../src/utils/todoHelpers';
import { Todo } from '../../src/types/todo';

// ---------------------------------------------------------------------------
// generateId
// ---------------------------------------------------------------------------

describe('generateId', () => {
  it('should return a non-empty string', () => {
    const id = generateId();
    expect(typeof id).toBe('string');
    expect(id.length).toBeGreaterThan(0);
  });

  it('should return unique values on successive calls', () => {
    const ids = new Set(Array.from({ length: 100 }, () => generateId()));
    expect(ids.size).toBe(100);
  });
});

// ---------------------------------------------------------------------------
// createTodo
// ---------------------------------------------------------------------------

describe('createTodo', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2024-01-15T12:00:00.000Z'));
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should create a todo with the given text', () => {
    const todo = createTodo('Buy groceries');
    expect(todo.text).toBe('Buy groceries');
  });

  it('should create a todo that is not completed', () => {
    const todo = createTodo('Buy groceries');
    expect(todo.completed).toBe(false);
  });

  it('should set createdAt to the current timestamp', () => {
    const now = Date.now();
    const todo = createTodo('Buy groceries');
    expect(todo.createdAt).toBe(now);
  });

  it('should assign a string id', () => {
    const todo = createTodo('Buy groceries');
    expect(typeof todo.id).toBe('string');
    expect(todo.id.length).toBeGreaterThan(0);
  });

  it('should produce unique ids for different todos', () => {
    const a = createTodo('Task A');
    const b = createTodo('Task B');
    expect(a.id).not.toBe(b.id);
  });
});

// ---------------------------------------------------------------------------
// toggleTodo
// ---------------------------------------------------------------------------

describe('toggleTodo', () => {
  const baseTodo: Todo = {
    id: 'test-1',
    text: 'Test todo',
    completed: false,
    createdAt: 1700000000000,
  };

  it('should flip completed from false to true', () => {
    const toggled = toggleTodo(baseTodo);
    expect(toggled.completed).toBe(true);
  });

  it('should flip completed from true to false', () => {
    const completedTodo: Todo = { ...baseTodo, completed: true };
    const toggled = toggleTodo(completedTodo);
    expect(toggled.completed).toBe(false);
  });

  it('should not mutate the original todo', () => {
    const original: Todo = { ...baseTodo };
    toggleTodo(original);
    expect(original.completed).toBe(false);
  });

  it('should preserve all other fields', () => {
    const toggled = toggleTodo(baseTodo);
    expect(toggled.id).toBe(baseTodo.id);
    expect(toggled.text).toBe(baseTodo.text);
    expect(toggled.createdAt).toBe(baseTodo.createdAt);
  });
});

// ---------------------------------------------------------------------------
// filterTodos
// ---------------------------------------------------------------------------

describe('filterTodos', () => {
  const todos: Todo[] = [
    { id: '1', text: 'Active 1', completed: false, createdAt: 1 },
    { id: '2', text: 'Completed 1', completed: true, createdAt: 2 },
    { id: '3', text: 'Active 2', completed: false, createdAt: 3 },
    { id: '4', text: 'Completed 2', completed: true, createdAt: 4 },
  ];

  it('should return all todos when filter is "all"', () => {
    const result = filterTodos(todos, 'all');
    expect(result).toHaveLength(4);
    expect(result).toEqual(todos);
  });

  it('should return only active todos when filter is "active"', () => {
    const result = filterTodos(todos, 'active');
    expect(result).toHaveLength(2);
    expect(result.every((t) => !t.completed)).toBe(true);
  });

  it('should return only completed todos when filter is "completed"', () => {
    const result = filterTodos(todos, 'completed');
    expect(result).toHaveLength(2);
    expect(result.every((t) => t.completed)).toBe(true);
  });

  it('should return an empty array when given an empty list', () => {
    expect(filterTodos([], 'all')).toEqual([]);
    expect(filterTodos([], 'active')).toEqual([]);
    expect(filterTodos([], 'completed')).toEqual([]);
  });

  it('should default to an empty array when todos is undefined', () => {
    // Explicit test for the default parameter
    expect(filterTodos(undefined as unknown as Todo[], 'all')).toEqual([]);
  });

  it('should not mutate the input array', () => {
    const copy = [...todos];
    filterTodos(todos, 'active');
    expect(todos).toEqual(copy);
  });

  it('should return an empty array for active filter when all are completed', () => {
    const allCompleted: Todo[] = [
      { id: '1', text: 'Done 1', completed: true, createdAt: 1 },
      { id: '2', text: 'Done 2', completed: true, createdAt: 2 },
    ];
    expect(filterTodos(allCompleted, 'active')).toEqual([]);
  });

  it('should return an empty array for completed filter when none are completed', () => {
    const noneCompleted: Todo[] = [
      { id: '1', text: 'Todo 1', completed: false, createdAt: 1 },
      { id: '2', text: 'Todo 2', completed: false, createdAt: 2 },
    ];
    expect(filterTodos(noneCompleted, 'completed')).toEqual([]);
  });
});
