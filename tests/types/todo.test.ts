/**
 * Tests for the Todo type definitions.
 *
 * These are structural/compile-time sanity checks that verify objects
 * conforming to the Todo interface and TodoFilter type are accepted.
 */

import { describe, it, expect } from 'vitest';
import { Todo, TodoFilter } from '../../src/types/todo';

describe('Todo interface', () => {
  it('should allow creating an object that satisfies the Todo shape', () => {
    const todo: Todo = {
      id: 'abc123',
      text: 'Write tests',
      completed: false,
      createdAt: 1700000000000,
    };

    expect(todo.id).toBe('abc123');
    expect(todo.text).toBe('Write tests');
    expect(todo.completed).toBe(false);
    expect(todo.createdAt).toBe(1700000000000);
  });

  it('should allow completed to be true', () => {
    const todo: Todo = {
      id: 'xyz789',
      text: 'Done task',
      completed: true,
      createdAt: 1700000000000,
    };

    expect(todo.completed).toBe(true);
  });
});

describe('TodoFilter type', () => {
  it('should accept all valid filter values', () => {
    const filters: TodoFilter[] = ['all', 'active', 'completed'];

    expect(filters).toHaveLength(3);
    expect(filters).toContain('all');
    expect(filters).toContain('active');
    expect(filters).toContain('completed');
  });
});
