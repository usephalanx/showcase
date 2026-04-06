/**
 * Core TypeScript type definitions for the Kanban application.
 * These mirror the backend Pydantic schemas.
 */

export interface Board {
  id: number;
  title: string;
  slug: string;
  description: string | null;
  created_at: string;
  updated_at: string;
  columns: Column[];
}

export interface BoardSummary {
  id: number;
  title: string;
  slug: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface Column {
  id: number;
  board_id: number;
  title: string;
  position: number;
  created_at: string;
  updated_at: string;
  cards: Card[];
}

export interface Card {
  id: number;
  column_id: number;
  title: string;
  slug: string;
  description: string | null;
  position: number;
  created_at: string;
  updated_at: string;
  tags: Tag[];
}

export interface Tag {
  id: number;
  name: string;
  color: string;
  created_at: string;
}

export interface CreateBoardRequest {
  title: string;
  description?: string;
}

export interface UpdateBoardRequest {
  title?: string;
  description?: string;
}

export interface CreateColumnRequest {
  title: string;
}

export interface UpdateColumnRequest {
  title?: string;
}

export interface MoveColumnRequest {
  position: number;
}

export interface CreateCardRequest {
  title: string;
  description?: string;
}

export interface UpdateCardRequest {
  title?: string;
  description?: string;
}

export interface MoveCardRequest {
  column_id: number;
  position: number;
}

export interface CreateTagRequest {
  name: string;
  color?: string;
}

export interface ApiError {
  detail: string;
}
