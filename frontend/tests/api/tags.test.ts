/**
 * Unit tests for the tagsApi service module.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import apiClient from '../../src/api/client';
import { tagsApi } from '../../src/api/tags';
import type { Tag } from '../../src/types';

vi.mock('../../src/api/client');

const mockedClient = vi.mocked(apiClient, true);

const sampleTag: Tag = {
  id: 1,
  name: 'Bug',
  slug: 'bug',
  color: '#e74c3c',
  created_at: '2024-01-01T00:00:00Z',
};

beforeEach(() => {
  vi.clearAllMocks();
});

describe('tagsApi', () => {
  describe('list', () => {
    it('should GET /tags and return data', async () => {
      mockedClient.get.mockResolvedValueOnce({ data: [sampleTag] });

      const result = await tagsApi.list();

      expect(mockedClient.get).toHaveBeenCalledWith('/tags');
      expect(result).toEqual([sampleTag]);
    });
  });

  describe('getBySlug', () => {
    it('should GET /tags/:slug and return the tag', async () => {
      mockedClient.get.mockResolvedValueOnce({ data: sampleTag });

      const result = await tagsApi.getBySlug('bug');

      expect(mockedClient.get).toHaveBeenCalledWith('/tags/bug');
      expect(result).toEqual(sampleTag);
    });
  });

  describe('create', () => {
    it('should POST /tags with payload and return created tag', async () => {
      const payload = { name: 'Bug', color: '#e74c3c' };
      mockedClient.post.mockResolvedValueOnce({ data: sampleTag });

      const result = await tagsApi.create(payload);

      expect(mockedClient.post).toHaveBeenCalledWith('/tags', payload);
      expect(result).toEqual(sampleTag);
    });

    it('should POST /tags with name only when color is omitted', async () => {
      const payload = { name: 'Feature' };
      const createdTag: Tag = {
        ...sampleTag,
        id: 2,
        name: 'Feature',
        slug: 'feature',
        color: '#3498db',
      };
      mockedClient.post.mockResolvedValueOnce({ data: createdTag });

      const result = await tagsApi.create(payload);

      expect(mockedClient.post).toHaveBeenCalledWith('/tags', payload);
      expect(result.name).toBe('Feature');
    });
  });

  describe('delete', () => {
    it('should DELETE /tags/:slug and return confirmation', async () => {
      const deleteResp = { detail: 'Tag deleted successfully' };
      mockedClient.delete.mockResolvedValueOnce({ data: deleteResp });

      const result = await tagsApi.delete('bug');

      expect(mockedClient.delete).toHaveBeenCalledWith('/tags/bug');
      expect(result).toEqual(deleteResp);
    });
  });
});
