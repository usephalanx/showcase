/**
 * Unit tests for the boardsApi service module.
 *
 * All HTTP calls are intercepted by mocking the shared apiClient so that
 * no real network requests are made.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import apiClient from '../../src/api/client';
import { boardsApi } from '../../src/api/boards';
import type { Board, BoardDetail } from '../../src/types';

vi.mock('../../src/api/client');

const mockedClient = vi.mocked(apiClient, true);

const sampleBoard: Board = {
  id: 1,
  name: 'My Board',
  slug: 'my-board',
  description: 'A test board',
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
};

const sampleBoardDetail: BoardDetail = {
  ...sampleBoard,
  columns: [],
};

beforeEach(() => {
  vi.clearAllMocks();
});

describe('boardsApi', () => {
  describe('list', () => {
    it('should GET /boards and return data', async () => {
      mockedClient.get.mockResolvedValueOnce({ data: [sampleBoard] });

      const result = await boardsApi.list();

      expect(mockedClient.get).toHaveBeenCalledWith('/boards');
      expect(result).toEqual([sampleBoard]);
    });
  });

  describe('getBySlug', () => {
    it('should GET /boards/:slug and return detailed board', async () => {
      mockedClient.get.mockResolvedValueOnce({ data: sampleBoardDetail });

      const result = await boardsApi.getBySlug('my-board');

      expect(mockedClient.get).toHaveBeenCalledWith('/boards/my-board');
      expect(result).toEqual(sampleBoardDetail);
    });
  });

  describe('create', () => {
    it('should POST /boards with payload and return created board', async () => {
      const payload = { name: 'New Board', description: 'desc' };
      mockedClient.post.mockResolvedValueOnce({ data: sampleBoard });

      const result = await boardsApi.create(payload);

      expect(mockedClient.post).toHaveBeenCalledWith('/boards', payload);
      expect(result).toEqual(sampleBoard);
    });
  });

  describe('update', () => {
    it('should PUT /boards/:slug with payload and return updated board', async () => {
      const payload = { name: 'Updated Name' };
      mockedClient.put.mockResolvedValueOnce({ data: { ...sampleBoard, name: 'Updated Name' } });

      const result = await boardsApi.update('my-board', payload);

      expect(mockedClient.put).toHaveBeenCalledWith('/boards/my-board', payload);
      expect(result.name).toBe('Updated Name');
    });
  });

  describe('delete', () => {
    it('should DELETE /boards/:slug and return confirmation', async () => {
      const deleteResp = { detail: 'Board deleted successfully' };
      mockedClient.delete.mockResolvedValueOnce({ data: deleteResp });

      const result = await boardsApi.delete('my-board');

      expect(mockedClient.delete).toHaveBeenCalledWith('/boards/my-board');
      expect(result).toEqual(deleteResp);
    });
  });
});
