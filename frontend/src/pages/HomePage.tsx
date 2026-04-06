import React, { useCallback, useEffect, useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { Link } from 'react-router-dom';

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

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

interface NewBoardPayload {
  title: string;
  description: string;
}

/* ------------------------------------------------------------------ */
/*  Inline sub-components (small enough to stay in page file)          */
/* ------------------------------------------------------------------ */

const SEOHead: React.FC = () => (
  <Helmet>
    <title>Kanban Boards | Your Workspace</title>
    <meta
      name="description"
      content="Browse and manage all your Kanban boards in one place. Create boards, organize tasks, and boost productivity with drag-and-drop task management."
    />
    <meta property="og:title" content="Kanban Boards | Your Workspace" />
    <meta
      property="og:description"
      content="Browse and manage all your Kanban boards in one place."
    />
    <meta property="og:type" content="website" />
    <link rel="canonical" href={`${window.location.origin}/`} />
    <script type="application/ld+json">
      {JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'WebPage',
        name: 'Kanban Boards | Your Workspace',
        description:
          'Browse and manage all your Kanban boards in one place. Create boards, organize tasks, and boost productivity.',
        url: `${window.location.origin}/`,
      })}
    </script>
  </Helmet>
);

const HeroSection: React.FC<{ onAddBoard: () => void }> = ({ onAddBoard }) => (
  <section
    style={{
      textAlign: 'center',
      padding: '3rem 1rem 2rem',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      borderRadius: '12px',
      marginBottom: '2rem',
      color: '#fff',
    }}
  >
    <h1 style={{ fontSize: '2.25rem', margin: '0 0 0.75rem', fontWeight: 700 }}>
      Your Workspace
    </h1>
    <p style={{ fontSize: '1.125rem', margin: '0 0 1.5rem', opacity: 0.9 }}>
      Organize your projects with beautiful Kanban boards. Drag, drop, and get things done.
    </p>
    <button
      type="button"
      onClick={onAddBoard}
      style={{
        padding: '0.75rem 1.75rem',
        fontSize: '1rem',
        fontWeight: 600,
        color: '#667eea',
        background: '#fff',
        border: 'none',
        borderRadius: '8px',
        cursor: 'pointer',
        transition: 'transform 0.15s ease, box-shadow 0.15s ease',
      }}
      aria-label="Add a new board"
    >
      + Add Board
    </button>
  </section>
);

interface BoardCardProps {
  board: Board;
}

const BoardCard: React.FC<BoardCardProps> = ({ board }) => (
  <Link
    to={`/boards/${board.slug}`}
    style={{
      display: 'block',
      padding: '1.5rem',
      border: '1px solid #e2e8f0',
      borderRadius: '10px',
      textDecoration: 'none',
      color: 'inherit',
      background: '#fff',
      transition: 'box-shadow 0.15s ease, transform 0.15s ease',
    }}
    aria-label={`Open board: ${board.title}`}
    onMouseEnter={(e) => {
      (e.currentTarget as HTMLElement).style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
      (e.currentTarget as HTMLElement).style.transform = 'translateY(-2px)';
    }}
    onMouseLeave={(e) => {
      (e.currentTarget as HTMLElement).style.boxShadow = 'none';
      (e.currentTarget as HTMLElement).style.transform = 'translateY(0)';
    }}
  >
    <h2 style={{ fontSize: '1.125rem', margin: '0 0 0.5rem', fontWeight: 600 }}>
      {board.title}
    </h2>
    {board.description && (
      <p style={{ margin: 0, color: '#718096', fontSize: '0.875rem', lineHeight: 1.5 }}>
        {board.description}
      </p>
    )}
    <p style={{ margin: '0.75rem 0 0', color: '#a0aec0', fontSize: '0.75rem' }}>
      Updated {new Date(board.updated_at).toLocaleDateString()}
    </p>
  </Link>
);

interface AddBoardModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (payload: NewBoardPayload) => void;
  submitting: boolean;
}

const AddBoardModal: React.FC<AddBoardModalProps> = ({ open, onClose, onSubmit, submitting }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    onSubmit({ title: title.trim(), description: description.trim() });
  };

  // Reset form when modal opens
  useEffect(() => {
    if (open) {
      setTitle('');
      setDescription('');
    }
  }, [open]);

  if (!open) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label="Add a new board"
      style={{
        position: 'fixed',
        inset: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        background: 'rgba(0,0,0,0.5)',
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        style={{
          background: '#fff',
          borderRadius: '12px',
          padding: '2rem',
          width: '100%',
          maxWidth: '480px',
          margin: '1rem',
          boxShadow: '0 20px 60px rgba(0,0,0,0.15)',
        }}
      >
        <h2 style={{ margin: '0 0 1.25rem', fontSize: '1.375rem', fontWeight: 600 }}>
          Create New Board
        </h2>
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1rem' }}>
            <label
              htmlFor="board-title"
              style={{ display: 'block', marginBottom: '0.375rem', fontWeight: 500, fontSize: '0.875rem' }}
            >
              Board Title *
            </label>
            <input
              id="board-title"
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Sprint Planning"
              autoFocus
              style={{
                width: '100%',
                padding: '0.625rem 0.75rem',
                border: '1px solid #e2e8f0',
                borderRadius: '6px',
                fontSize: '1rem',
                boxSizing: 'border-box',
              }}
            />
          </div>
          <div style={{ marginBottom: '1.5rem' }}>
            <label
              htmlFor="board-description"
              style={{ display: 'block', marginBottom: '0.375rem', fontWeight: 500, fontSize: '0.875rem' }}
            >
              Description
            </label>
            <textarea
              id="board-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Optional description…"
              rows={3}
              style={{
                width: '100%',
                padding: '0.625rem 0.75rem',
                border: '1px solid #e2e8f0',
                borderRadius: '6px',
                fontSize: '1rem',
                resize: 'vertical',
                boxSizing: 'border-box',
              }}
            />
          </div>
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
            <button
              type="button"
              onClick={onClose}
              disabled={submitting}
              style={{
                padding: '0.625rem 1.25rem',
                fontSize: '0.875rem',
                background: '#edf2f7',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
              }}
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting || !title.trim()}
              style={{
                padding: '0.625rem 1.25rem',
                fontSize: '0.875rem',
                background: '#667eea',
                color: '#fff',
                border: 'none',
                borderRadius: '6px',
                cursor: submitting || !title.trim() ? 'not-allowed' : 'pointer',
                opacity: submitting || !title.trim() ? 0.6 : 1,
              }}
            >
              {submitting ? 'Creating…' : 'Create Board'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

const EmptyState: React.FC<{ onAddBoard: () => void }> = ({ onAddBoard }) => (
  <div
    style={{
      textAlign: 'center',
      padding: '4rem 2rem',
      border: '2px dashed #e2e8f0',
      borderRadius: '12px',
      color: '#a0aec0',
    }}
  >
    <p style={{ fontSize: '1.125rem', margin: '0 0 0.5rem' }}>
      No boards yet
    </p>
    <p style={{ margin: '0 0 1.5rem', fontSize: '0.875rem' }}>
      Create your first board to get started!
    </p>
    <button
      type="button"
      onClick={onAddBoard}
      style={{
        padding: '0.625rem 1.5rem',
        fontSize: '0.9375rem',
        fontWeight: 600,
        background: '#667eea',
        color: '#fff',
        border: 'none',
        borderRadius: '8px',
        cursor: 'pointer',
      }}
    >
      + Create First Board
    </button>
  </div>
);

/* ------------------------------------------------------------------ */
/*  Main page component                                                */
/* ------------------------------------------------------------------ */

const HomePage: React.FC = () => {
  const [boards, setBoards] = useState<Board[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const fetchBoards = useCallback(async (): Promise<void> => {
    try {
      setLoading(true);
      const response = await fetch('/api/boards');
      if (!response.ok) {
        throw new Error(`Failed to load boards (HTTP ${response.status})`);
      }
      const data: Board[] = await response.json();
      setBoards(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/boards');
        if (!response.ok) throw new Error(`Failed to load boards (HTTP ${response.status})`);
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
        if (!cancelled) setLoading(false);
      }
    };

    void load();
    return () => { cancelled = true; };
  }, []);

  const handleCreateBoard = async (payload: NewBoardPayload) => {
    try {
      setSubmitting(true);
      const response = await fetch('/api/boards', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        throw new Error(`Failed to create board (HTTP ${response.status})`);
      }
      const newBoard: Board = await response.json();
      setBoards((prev) => [newBoard, ...prev]);
      setModalOpen(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create board.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      <SEOHead />

      <div
        className="home-page"
        style={{ maxWidth: '1200px', margin: '0 auto', padding: '1.5rem 1rem' }}
      >
        <HeroSection onAddBoard={() => setModalOpen(true)} />

        {loading && (
          <p className="home-page__loading" role="status" style={{ textAlign: 'center', color: '#718096' }}>
            Loading boards…
          </p>
        )}

        {error && (
          <p className="home-page__error" role="alert" style={{ color: '#e53e3e', textAlign: 'center' }}>
            {error}
          </p>
        )}

        {!loading && !error && boards.length === 0 && (
          <EmptyState onAddBoard={() => setModalOpen(true)} />
        )}

        {!loading && !error && boards.length > 0 && (
          <ul
            className="home-page__board-list"
            style={{
              listStyle: 'none',
              padding: 0,
              margin: 0,
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
              gap: '1.25rem',
            }}
          >
            {boards.map((board) => (
              <li key={board.id}>
                <BoardCard board={board} />
              </li>
            ))}
          </ul>
        )}
      </div>

      <AddBoardModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleCreateBoard}
        submitting={submitting}
      />
    </>
  );
};

export default HomePage;
