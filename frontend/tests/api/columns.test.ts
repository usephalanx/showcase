/**
 * Unit tests for the columnsApi service module.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import apiClient from '../../src/api/client';
import { columnsApi } from '../../src/api/columns';
import type { Column } from '../../src/types';

vi.mock('../../src/api/client');

const mockedClient = vi.mocked(apiClient, true);

const sampleColumn: Column = {
  id: 1,
  title: 'To Do',
  position: 0,
  board_id: 1,
  cards: [],
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
};

beforeEach(() => {
  vi.clearAllMocks();
});

describe('columnsApi', () => {
  describe('create', () => {
    it('should POST /columns with payload', async () => {
      const payload = { title: 'To Do', board_id: 1 };
      mockedClient.post.mockResolvedValueOnce({ data: sampleColumn });

      const result = await columnsApi.create(payload);

      expect(mockedClient.post).toHaveBeenCalledWith('/columns', payload);
      expect(result).toEqual(sampleColumn);
    });
  });

  describe('update', () => {
    it('should PUT /columns/:id with payload', async () => {
      const payload = { title: 'Done' };
      mockedClient.put.mockResolvedValueOnce({ data: { ...sampleColumn, title: 'Done' } });

      const result = await columnsApi.update(1, payload);

      expect(mockedClient.put).toHaveBeenCalledWith('/columns/1', payload);
      expect(result.title).toBe('Done');
    });
  });

  describe('delete', () => {
    it('should DELETE /columns/:id', async () => {
      const deleteResp = { detail: 'Column deleted successfully' };
      mockedClient.delete.mockResolvedValueOnce({ data: deleteResp });

      const result = await columnsApi.delete(1);

      expect(mockedClient.delete).toHaveBeenCalledWith('/columns/1');
      expect(result).toEqual(deleteResp);
    });
  });

  describe('reorder', () => {
    it('should PUT /boards/:boardId/columns/reorder with column_ids', async () => {
      const payload = { column_ids: [3, 1, 2] };
      mockedClient.put.mockResolvedValueOnce({ data: [sampleColumn] });

      const result = await columnsApi.reorder(1, payload);

      expect(mockedClient.put).toHaveBeenCalledWith(
        '/boards/1/columns/reorder',
        payload,
      );
      expect(result).toEqual([sampleColumn]);
    });
  });
});
