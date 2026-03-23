/**
 * Shared TypeScript type definitions for the frontend application.
 */

/** A project as returned by the API. */
export interface Project {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
}

/** Payload for creating a new project. */
export interface ProjectCreatePayload {
  name: string;
  description: string;
}
