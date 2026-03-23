/**
 * Custom hook for managing project state (fetch, create, delete).
 */

import { useCallback, useEffect, useState } from 'react';
import type { Project, ProjectCreatePayload } from '../types';
import {
  fetchProjects as apiFetchProjects,
  createProject as apiCreateProject,
  deleteProject as apiDeleteProject,
} from '../api/projects';

export interface UseProjectsReturn {
  /** The list of projects. */
  projects: Project[];
  /** Whether the initial fetch is in progress. */
  loading: boolean;
  /** Any error message from the most recent operation. */
  error: string | null;
  /** Create a new project and add it to the list. */
  addProject: (payload: ProjectCreatePayload) => Promise<void>;
  /** Delete a project by ID and remove it from the list. */
  removeProject: (id: number) => Promise<void>;
  /** Re-fetch all projects from the API. */
  refresh: () => Promise<void>;
}

/**
 * Hook to manage the projects collection.
 */
export function useProjects(): UseProjectsReturn {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetchProjects();
      setProjects(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load projects');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const addProject = useCallback(async (payload: ProjectCreatePayload) => {
    setError(null);
    try {
      const created = await apiCreateProject(payload);
      setProjects((prev) => [created, ...prev]);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to create project';
      setError(message);
      throw err;
    }
  }, []);

  const removeProject = useCallback(async (id: number) => {
    setError(null);
    // Optimistic removal
    setProjects((prev) => prev.filter((p) => p.id !== id));
    try {
      await apiDeleteProject(id);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to delete project';
      setError(message);
      // Re-fetch to restore correct state
      try {
        const data = await apiFetchProjects();
        setProjects(data);
      } catch {
        // keep error from delete
      }
    }
  }, []);

  return { projects, loading, error, addProject, removeProject, refresh };
}
