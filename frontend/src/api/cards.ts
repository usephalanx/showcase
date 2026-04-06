/**
 * API service for Card operations.
 *
 * Cards live inside columns and can be moved between them.  Tags can
 * be assigned to and removed from individual cards.
 */

import apiClient from './client';
import type {
  Card,
  CardCreate,
  CardMove,
  CardTagAction,
  CardUpdate,
  DeleteResponse,
} from '../types';

/** Namespace for card-related API calls. */
export const cardsApi = {
  /**
   * Create a new card.
   *
   * @param data - The card creation payload (must include column_id).
   * @returns A promise that resolves to the newly created card.
   */
  async create(data: CardCreate): Promise<Card> {
    const response = await apiClient.post<Card>('/cards', data);
    return response.data;
  },

  /**
   * Update an existing card's content fields.
   *
   * @param cardId - The numeric id of the card.
   * @param data - The fields to update.
   * @returns A promise that resolves to the updated card.
   */
  async update(cardId: number, data: CardUpdate): Promise<Card> {
    const response = await apiClient.put<Card>(`/cards/${cardId}`, data);
    return response.data;
  },

  /**
   * Delete a card by its id.
   *
   * @param cardId - The numeric id of the card to delete.
   * @returns A promise that resolves to the deletion confirmation.
   */
  async delete(cardId: number): Promise<DeleteResponse> {
    const response = await apiClient.delete<DeleteResponse>(`/cards/${cardId}`);
    return response.data;
  },

  /**
   * Move a card to a (possibly different) column and/or position.
   *
   * @param cardId - The numeric id of the card to move.
   * @param data - The target column_id and position.
   * @returns A promise that resolves to the updated card.
   */
  async move(cardId: number, data: CardMove): Promise<Card> {
    const response = await apiClient.put<Card>(`/cards/${cardId}/move`, data);
    return response.data;
  },

  /**
   * Assign a tag to a card.
   *
   * @param cardId - The numeric id of the card.
   * @param data - Object containing the tag_id to assign.
   * @returns A promise that resolves to the updated card.
   */
  async assignTag(cardId: number, data: CardTagAction): Promise<Card> {
    const response = await apiClient.post<Card>(`/cards/${cardId}/tags`, data);
    return response.data;
  },

  /**
   * Remove a tag from a card.
   *
   * @param cardId - The numeric id of the card.
   * @param tagId - The numeric id of the tag to remove.
   * @returns A promise that resolves to the deletion confirmation.
   */
  async removeTag(cardId: number, tagId: number): Promise<DeleteResponse> {
    const response = await apiClient.delete<DeleteResponse>(
      `/cards/${cardId}/tags/${tagId}`,
    );
    return response.data;
  },
};
