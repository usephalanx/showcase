/**
 * API service for Tag operations.
 *
 * Tags are global entities that can be assigned to any card across boards.
 */

import apiClient from './client';
import type { DeleteResponse, Tag, TagCreate } from '../types';

/** Namespace for tag-related API calls. */
export const tagsApi = {
  /**
   * Fetch all tags.
   *
   * @returns A promise that resolves to the list of tags.
   */
  async list(): Promise<Tag[]> {
    const response = await apiClient.get<Tag[]>('/tags');
    return response.data;
  },

  /**
   * Fetch a single tag by its slug.
   *
   * @param slug - The URL-safe slug of the tag.
   * @returns A promise that resolves to the tag.
   */
  async getBySlug(slug: string): Promise<Tag> {
    const response = await apiClient.get<Tag>(`/tags/${slug}`);
    return response.data;
  },

  /**
   * Create a new tag.
   *
   * @param data - The tag creation payload.
   * @returns A promise that resolves to the newly created tag.
   */
  async create(data: TagCreate): Promise<Tag> {
    const response = await apiClient.post<Tag>('/tags', data);
    return response.data;
  },

  /**
   * Delete a tag by its slug.
   *
   * @param slug - The URL-safe slug of the tag to delete.
   * @returns A promise that resolves to the deletion confirmation.
   */
  async delete(slug: string): Promise<DeleteResponse> {
    const response = await apiClient.delete<DeleteResponse>(`/tags/${slug}`);
    return response.data;
  },
};
