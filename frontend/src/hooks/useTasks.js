import { useState, useEffect, useCallback } from 'react';
import { fetchTasks } from '../api/tasks';

/**
 * Custom hook for fetching tasks, optionally filtered by project ID.
 *
 * @param {number|string|null} projectId - Optional project ID filter.
 * @returns {{ tasks: Array, loading: boolean, error: string|null, refetch: function }}
 */
export function useTasks(projectId = null) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchTasks(projectId);
      setTasks(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    refetch();
  }, [refetch]);

  return { tasks, loading, error, refetch };
}
