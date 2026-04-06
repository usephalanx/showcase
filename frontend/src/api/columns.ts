/**
 * API service for Column operations.
 *
 * Columns belong to a board.  The reorder endpoint accepts a full
 * ordered list of column ids for a given board.
 */

import apiClient from './client';
import type {
  Column,
  ColumnCreate,
  ColumnReorder,
  ColumnUpdate,
  DeleteResponse,
} from '../types';

/** Namespace for column-related API calls. */
export const columnsApi = {
  /**
   * Create a new column.
   *
   * @param data - The column creation payload (must include board_id).
   * @returns A promise that resolves to the newly created column.
   */
  async create(data: ColumnCreate): Promise<Column> {
    const response = await apiClient.post<Column>('/columns', data);
    return response.data;
  },

  /**
   * Update an existing column.
   *
   * @param columnId - The numeric id of the column.
   * @param data - The fields to update.
   * @returns A promise that resolves to the updated column.
   */
  async update(columnId: number, data: ColumnUpdate): Promise<Column> {
    const response = await apiClient.put<Column>(`/columns/${columnId}`, data);
    return response.data;
  },

  /**
   * Delete a column by its id.
   *
   * @param columnId - The numeric id of the column to delete.
   * @returns A promise that resolves to the deletion confirmation.
   */
  async delete(columnId: number): Promise<DeleteResponse> {
    const response = await apiClient.delete<DeleteResponse>(
      `/columns/${columnId}`,
    );
    return response.data;
  },

  /**
   * Reorder all columns within a board.
   *
   * The backend expects an ordered array of column ids; the position of
   * each column is derived from its index in the array.
   *
   * @param boardId - The numeric id of the board whose columns are being reordered.
   * @param data - Object containing the ordered column_ids array.
   * @returns A promise that resolves to the reordered columns.
   */
  async reorder(boardId: number, data: ColumnReorder): Promise<Column[]> {
    const response = await apiClient.put<Column[]>(
      `/boards/${boardId}/columns/reorder`,
      data,
    );
    return response.data;
  },
};
