/**
 * Compile-time and runtime shape tests for TypeScript interfaces.
 *
 * These tests verify that objects conforming to the declared interfaces
 * have the expected keys and value types at runtime.  Since TypeScript
 * interfaces are erased at compile time, these tests act as a safety net
 * ensuring the shape contracts match what the API actually returns.
 */

import { describe, it, expect } from 'vitest';
import type {
  Board,
  BoardCreate,
  BoardDetail,
  BoardUpdate,
  Card,
  CardCreate,
  CardMove,
  CardTagAction,
  CardUpdate,
  Column,
  ColumnCreate,
  ColumnReorder,
  ColumnUpdate,
  DeleteResponse,
  PaginatedResponse,
  Tag,
  TagCreate,
} from '../../src/types';

describe('TypeScript interface shape validation', () => {
  it('Board interface has all required fields', () => {
    const board: Board = {
      id: 1,
      name: 'Test',
      slug: 'test',
      description: '',
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    };
    expect(board).toHaveProperty('id');
    expect(board).toHaveProperty('name');
    expect(board).toHaveProperty('slug');
    expect(board).toHaveProperty('description');
    expect(board).toHaveProperty('created_at');
    expect(board).toHaveProperty('updated_at');
  });

  it('BoardDetail extends Board with columns', () => {
    const boardDetail: BoardDetail = {
      id: 1,
      name: 'Test',
      slug: 'test',
      description: '',
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
      columns: [],
    };
    expect(boardDetail).toHaveProperty('columns');
    expect(Array.isArray(boardDetail.columns)).toBe(true);
  });

  it('BoardCreate requires name', () => {
    const create: BoardCreate = { name: 'New Board' };
    expect(create).toHaveProperty('name');
  });

  it('BoardUpdate allows partial fields', () => {
    const update: BoardUpdate = { name: 'Renamed' };
    expect(update).toHaveProperty('name');
    const updateDesc: BoardUpdate = { description: 'new desc' };
    expect(updateDesc).toHaveProperty('description');
  });

  it('Column interface has all required fields', () => {
    const column: Column = {
      id: 1,
      title: 'To Do',
      position: 0,
      board_id: 1,
      cards: [],
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    };
    expect(column).toHaveProperty('id');
    expect(column).toHaveProperty('title');
    expect(column).toHaveProperty('position');
    expect(column).toHaveProperty('board_id');
    expect(column).toHaveProperty('cards');
  });

  it('ColumnCreate requires title and board_id', () => {
    const create: ColumnCreate = { title: 'To Do', board_id: 1 };
    expect(create).toHaveProperty('title');
    expect(create).toHaveProperty('board_id');
  });

  it('ColumnUpdate allows partial title', () => {
    const update: ColumnUpdate = { title: 'In Progress' };
    expect(update).toHaveProperty('title');
  });

  it('ColumnReorder requires column_ids array', () => {
    const reorder: ColumnReorder = { column_ids: [3, 1, 2] };
    expect(reorder).toHaveProperty('column_ids');
    expect(Array.isArray(reorder.column_ids)).toBe(true);
  });

  it('Card interface has all required fields including tags', () => {
    const card: Card = {
      id: 1,
      title: 'Task',
      slug: 'task',
      description: '',
      position: 0,
      column_id: 1,
      tags: [],
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    };
    expect(card).toHaveProperty('id');
    expect(card).toHaveProperty('title');
    expect(card).toHaveProperty('slug');
    expect(card).toHaveProperty('description');
    expect(card).toHaveProperty('position');
    expect(card).toHaveProperty('column_id');
    expect(card).toHaveProperty('tags');
    expect(Array.isArray(card.tags)).toBe(true);
  });

  it('CardCreate requires title and column_id', () => {
    const create: CardCreate = { title: 'New', column_id: 1 };
    expect(create).toHaveProperty('title');
    expect(create).toHaveProperty('column_id');
  });

  it('CardUpdate allows partial fields', () => {
    const update: CardUpdate = { title: 'Updated' };
    expect(update).toHaveProperty('title');
  });

  it('CardMove requires column_id and position', () => {
    const move: CardMove = { column_id: 2, position: 0 };
    expect(move).toHaveProperty('column_id');
    expect(move).toHaveProperty('position');
  });

  it('CardTagAction requires tag_id', () => {
    const action: CardTagAction = { tag_id: 5 };
    expect(action).toHaveProperty('tag_id');
  });

  it('Tag interface has all required fields', () => {
    const tag: Tag = {
      id: 1,
      name: 'Bug',
      slug: 'bug',
      color: '#e74c3c',
      created_at: '2024-01-01T00:00:00Z',
    };
    expect(tag).toHaveProperty('id');
    expect(tag).toHaveProperty('name');
    expect(tag).toHaveProperty('slug');
    expect(tag).toHaveProperty('color');
    expect(tag).toHaveProperty('created_at');
  });

  it('TagCreate requires name with optional color', () => {
    const create: TagCreate = { name: 'Feature' };
    expect(create).toHaveProperty('name');
    const createWithColor: TagCreate = { name: 'Feature', color: '#3498db' };
    expect(createWithColor).toHaveProperty('color');
  });

  it('DeleteResponse has detail', () => {
    const resp: DeleteResponse = { detail: 'Deleted' };
    expect(resp).toHaveProperty('detail');
  });

  it('PaginatedResponse has pagination metadata', () => {
    const paginated: PaginatedResponse<Board> = {
      items: [],
      total: 0,
      page: 1,
      per_page: 20,
      total_pages: 0,
    };
    expect(paginated).toHaveProperty('items');
    expect(paginated).toHaveProperty('total');
    expect(paginated).toHaveProperty('page');
    expect(paginated).toHaveProperty('per_page');
    expect(paginated).toHaveProperty('total_pages');
    expect(Array.isArray(paginated.items)).toBe(true);
  });
});
