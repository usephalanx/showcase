/**
 * API service for Board CRUD operations.
 *
 * All functions communicate with the FastAPI backend through the shared
 * axios client and return strongly-typed promises.
 */

import apiClient from './client';
import type {
  Board,
  BoardCreate,
  BoardDetail,
  BoardUpdate,
  DeleteResponse,
} from '../types';

/** Namespace for board-related API calls. */
export const boardsApi = {
  /**
   * Fetch all boards.
   *
   * @returns A promise that resolves to the list of boards.
   */
  async list(): Promise<Board[]> {
    const response = await apiClient.get<Board[]>('/boards');
    return response.data;
  },

  /**
   * Fetch a single board by its slug, including nested columns and cards.
   *
   * @param slug - The URL-safe slug of the board.
   * @returns A promise that resolves to the detailed board.
   */
  async getBySlug(slug: string): Promise<BoardDetail> {
    const response = await apiClient.get<BoardDetail>(`/boards/${slug}`);
    return response.data;
  },

  /**
   * Create a new board.
   *
   * @param data - The board creation payload.
   * @returns A promise that resolves to the newly created board.
   */
  async create(data: BoardCreate): Promise<Board> {
    const response = await apiClient.post<Board>('/boards', data);
    return response.data;
  },

  /**
   * Update an existing board.
   *
   * @param slug - The URL-safe slug of the board to update.
   * @param data - The fields to update.
   * @returns A promise that resolves to the updated board.
   */
  async update(slug: string, data: BoardUpdate): Promise<Board> {
    const response = await apiClient.put<Board>(`/boards/${slug}`, data);
    return response.data;
  },

  /**
   * Delete a board by its slug.
   *
   * @param slug - The URL-safe slug of the board to delete.
   * @returns A promise that resolves to the deletion confirmation.
   */
  async delete(slug: string): Promise<DeleteResponse> {
    const response = await apiClient.delete<DeleteResponse>(`/boards/${slug}`);
    return response.data;
  },
};
