import { useState, useEffect, useCallback } from 'react';
import { fetchProjects, fetchProject } from '../api/projects';

/**
 * Custom hook for fetching the list of projects.
 *
 * @returns {{ projects: Array, loading: boolean, error: string|null, refetch: function }}
 */
export function useProjects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchProjects();
      setProjects(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch projects');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refetch();
  }, [refetch]);

  return { projects, loading, error, refetch };
}

/**
 * Custom hook for fetching a single project by ID.
 *
 * @param {number|string} projectId - The project ID.
 * @returns {{ project: Object|null, loading: boolean, error: string|null, refetch: function }}
 */
export function useProject(projectId) {
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refetch = useCallback(async () => {
    if (!projectId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await fetchProject(projectId);
      setProject(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch project');
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    refetch();
  }, [refetch]);

  return { project, loading, error, refetch };
}
