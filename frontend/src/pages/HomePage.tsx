import React, { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { Link } from 'react-router-dom';

/**
 * Shape of a Board returned from the API.
 */
interface Board {
  id: number;
  title: string;
  slug: string;
  description: string | null;
  meta_title: string | null;
  meta_description: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * Home page component.
 *
 * Displays a list of all Kanban boards. Each board links to its
 * SEO-friendly slug-based URL at /boards/:slug.
 */
const HomePage: React.FC = () => {
  const [boards, setBoards] = useState<Board[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const fetchBoards = async (): Promise<void> => {
      try {
        setLoading(true);
        const response = await fetch('/api/boards');
        if (!response.ok) {
          throw new Error(`Failed to load boards (HTTP ${response.status})`);
        }
        const data: Board[] = await response.json();
        if (!cancelled) {
          setBoards(data);
          setError(null);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'An unexpected error occurred.');
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    void fetchBoards();

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <>
      <Helmet>
        <title>All Boards — Kanban Board</title>
        <meta
          name="description"
          content="Browse all Kanban boards. Organize your projects with drag-and-drop task management."
        />
        <meta property="og:title" content="All Boards — Kanban Board" />
        <meta
          property="og:description"
          content="Browse all Kanban boards and start organizing your projects."
        />
        <link rel="canonical" href={`${window.location.origin}/`} />
      </Helmet>

      <div className="home-page">
        <h1 style={{ fontSize: '1.75rem', marginBottom: '1.5rem' }}>Your Boards</h1>

        {loading && (
          <p className="home-page__loading" role="status">
            Loading boards…
          </p>
        )}

        {error && (
          <p className="home-page__error" role="alert" style={{ color: '#e53e3e' }}>
            {error}
          </p>
        )}

        {!loading && !error && boards.length === 0 && (
          <div className="home-page__empty">
            <p>No boards yet. Create your first board to get started!</p>
          </div>
        )}

        {!loading && !error && boards.length > 0 && (
          <ul
            className="home-page__board-list"
            style={{
              listStyle: 'none',
              padding: 0,
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
              gap: '1rem',
            }}
          >
            {boards.map((board) => (
              <li key={board.id}>
                <Link
                  to={`/boards/${board.slug}`}
                  style={{
                    display: 'block',
                    padding: '1.25rem',
                    border: '1px solid #e2e8f0',
                    borderRadius: '8px',
                    textDecoration: 'none',
                    color: 'inherit',
                    transition: 'box-shadow 0.15s ease',
                  }}
                  aria-label={`Open board: ${board.title}`}
                >
                  <h2 style={{ fontSize: '1.125rem', margin: '0 0 0.5rem' }}>{board.title}</h2>
                  {board.description && (
                    <p style={{ margin: 0, color: '#718096', fontSize: '0.875rem' }}>
                      {board.description}
                    </p>
                  )}
                </Link>
              </li>
            ))}
          </ul>
        )}
      </div>
    </>
  );
};

export default HomePage;
