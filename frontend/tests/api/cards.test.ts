/**
 * Unit tests for the cardsApi service module.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import apiClient from '../../src/api/client';
import { cardsApi } from '../../src/api/cards';
import type { Card } from '../../src/types';

vi.mock('../../src/api/client');

const mockedClient = vi.mocked(apiClient, true);

const sampleCard: Card = {
  id: 1,
  title: 'My Card',
  slug: 'my-card',
  description: 'Card description',
  position: 0,
  column_id: 1,
  tags: [],
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
};

beforeEach(() => {
  vi.clearAllMocks();
});

describe('cardsApi', () => {
  describe('create', () => {
    it('should POST /cards with payload', async () => {
      const payload = { title: 'My Card', column_id: 1 };
      mockedClient.post.mockResolvedValueOnce({ data: sampleCard });

      const result = await cardsApi.create(payload);

      expect(mockedClient.post).toHaveBeenCalledWith('/cards', payload);
      expect(result).toEqual(sampleCard);
    });
  });

  describe('update', () => {
    it('should PUT /cards/:id with payload', async () => {
      const payload = { title: 'Updated Card' };
      mockedClient.put.mockResolvedValueOnce({
        data: { ...sampleCard, title: 'Updated Card' },
      });

      const result = await cardsApi.update(1, payload);

      expect(mockedClient.put).toHaveBeenCalledWith('/cards/1', payload);
      expect(result.title).toBe('Updated Card');
    });
  });

  describe('delete', () => {
    it('should DELETE /cards/:id', async () => {
      const deleteResp = { detail: 'Card deleted successfully' };
      mockedClient.delete.mockResolvedValueOnce({ data: deleteResp });

      const result = await cardsApi.delete(1);

      expect(mockedClient.delete).toHaveBeenCalledWith('/cards/1');
      expect(result).toEqual(deleteResp);
    });
  });

  describe('move', () => {
    it('should PUT /cards/:id/move with column_id and position', async () => {
      const payload = { column_id: 2, position: 3 };
      mockedClient.put.mockResolvedValueOnce({
        data: { ...sampleCard, column_id: 2, position: 3 },
      });

      const result = await cardsApi.move(1, payload);

      expect(mockedClient.put).toHaveBeenCalledWith('/cards/1/move', payload);
      expect(result.column_id).toBe(2);
      expect(result.position).toBe(3);
    });
  });

  describe('assignTag', () => {
    it('should POST /cards/:id/tags with tag_id', async () => {
      const payload = { tag_id: 5 };
      const cardWithTag: Card = {
        ...sampleCard,
        tags: [
          {
            id: 5,
            name: 'Urgent',
            slug: 'urgent',
            color: '#ff0000',
            created_at: '2024-01-01T00:00:00Z',
          },
        ],
      };
      mockedClient.post.mockResolvedValueOnce({ data: cardWithTag });

      const result = await cardsApi.assignTag(1, payload);

      expect(mockedClient.post).toHaveBeenCalledWith('/cards/1/tags', payload);
      expect(result.tags).toHaveLength(1);
      expect(result.tags[0].name).toBe('Urgent');
    });
  });

  describe('removeTag', () => {
    it('should DELETE /cards/:id/tags/:tagId', async () => {
      const deleteResp = { detail: 'Tag removed from card' };
      mockedClient.delete.mockResolvedValueOnce({ data: deleteResp });

      const result = await cardsApi.removeTag(1, 5);

      expect(mockedClient.delete).toHaveBeenCalledWith('/cards/1/tags/5');
      expect(result).toEqual(deleteResp);
    });
  });
});
