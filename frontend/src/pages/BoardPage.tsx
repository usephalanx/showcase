import React, { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { useParams, Link } from 'react-router-dom';

/**
 * Shape of a Card inside a column.
 */
interface Card {
  id: number;
  title: string;
  slug: string;
  description: string | null;
  position: number;
}

/**
 * Shape of a Column inside a board.
 */
interface ColumnData {
  id: number;
  title: string;
  position: number;
  cards: Card[];
}

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
  columns: ColumnData[];
  created_at: string;
  updated_at: string;
}

/**
 * Board page component (Kanban view).
 *
 * Fetches a single board by its slug from the URL parameter and
 * renders its columns and cards in a horizontal Kanban layout.
 */
const BoardPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const [board, setBoard] = useState<Board | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const fetchBoard = async (): Promise<void> => {
      if (!slug) return;
      try {
        setLoading(true);
        const response = await fetch(`/api/boards/${slug}`);
        if (!response.ok) {
          if (response.status === 404) {
            throw new Error('Board not found.');
          }
          throw new Error(`Failed to load board (HTTP ${response.status})`);
        }
        const data: Board = await response.json();
        if (!cancelled) {
          setBoard(data);
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

    void fetchBoard();

    return () => {
      cancelled = true;
    };
  }, [slug]);

  const pageTitle = board?.meta_title ?? (board ? `${board.title} — Kanban Board` : 'Board — Kanban Board');
  const pageDescription =
    board?.meta_description ??
    (board?.description ?? 'View and manage your Kanban board columns and cards.');

  return (
    <>
      <Helmet>
        <title>{pageTitle}</title>
        <meta name="description" content={pageDescription} />
        <meta property="og:title" content={pageTitle} />
        <meta property="og:description" content={pageDescription} />
        {slug && <link rel="canonical" href={`${window.location.origin}/boards/${slug}`} />}
      </Helmet>

      <div className="board-page">
        {loading && (
          <p className="board-page__loading" role="status">
            Loading board…
          </p>
        )}

        {error && (
          <div className="board-page__error">
            <p role="alert" style={{ color: '#e53e3e' }}>
              {error}
            </p>
            <Link to="/">← Back to all boards</Link>
          </div>
        )}

        {!loading && !error && board && (
          <>
            <div
              className="board-page__header"
              style={{
                marginBottom: '1.5rem',
                display: 'flex',
                alignItems: 'center',
                gap: '1rem',
              }}
            >
              <Link to="/" style={{ color: '#3182ce', textDecoration: 'none' }}>
                ← Boards
              </Link>
              <h1 style={{ fontSize: '1.5rem', margin: 0 }}>{board.title}</h1>
            </div>

            {board.description && (
              <p
                className="board-page__description"
                style={{ color: '#718096', marginBottom: '1.5rem' }}
              >
                {board.description}
              </p>
            )}

            {board.columns.length === 0 ? (
              <div className="board-page__empty">
                <p>This board has no columns yet. Add a column to get started!</p>
              </div>
            ) : (
              <div
                className="board-page__columns"
                style={{
                  display: 'flex',
                  gap: '1rem',
                  overflowX: 'auto',
                  paddingBottom: '1rem',
                }}
              >
                {board.columns.map((column) => (
                  <div
                    key={column.id}
                    className="board-page__column"
                    style={{
                      minWidth: '280px',
                      maxWidth: '320px',
                      backgroundColor: '#f7fafc',
                      borderRadius: '8px',
                      padding: '1rem',
                      flex: '0 0 auto',
                    }}
                  >
                    <h2
                      style={{
                        fontSize: '1rem',
                        fontWeight: 600,
                        marginBottom: '0.75rem',
                        color: '#2d3748',
                      }}
                    >
                      {column.title}
                    </h2>
                    <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                      {column.cards.map((card) => (
                        <li key={card.id} style={{ marginBottom: '0.5rem' }}>
                          <Link
                            to={`/cards/${card.slug}`}
                            style={{
                              display: 'block',
                              padding: '0.75rem',
                              backgroundColor: '#ffffff',
                              border: '1px solid #e2e8f0',
                              borderRadius: '6px',
                              textDecoration: 'none',
                              color: '#1a202c',
                              fontSize: '0.875rem',
                            }}
                            aria-label={`View card: ${card.title}`}
                          >
                            {card.title}
                          </Link>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </>
  );
};

export default BoardPage;
