import React, { useEffect, useState, useCallback } from 'react';
import { Helmet } from 'react-helmet-async';
import { useParams, Link, useNavigate } from 'react-router-dom';

/**
 * Shape of a Category associated with a card.
 */
interface Category {
  id: number;
  name: string;
  slug: string;
}

/**
 * Column info returned alongside a card.
 */
interface ColumnInfo {
  id: number;
  title: string;
  board_id: number;
}

/**
 * Board info returned alongside a card.
 */
interface BoardInfo {
  id: number;
  title: string;
  slug: string;
}

/**
 * Full card detail shape from the API.
 */
interface CardDetail {
  id: number;
  title: string;
  slug: string;
  description: string | null;
  meta_title: string | null;
  meta_description: string | null;
  column_id: number;
  position: number;
  categories: Category[];
  created_at: string;
  updated_at: string;
  column?: ColumnInfo | null;
  board?: BoardInfo | null;
}

/**
 * Formats an ISO date string into a human-readable format.
 */
function formatDate(iso: string): string {
  try {
    return new Date(iso).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return iso;
  }
}

/**
 * CardDetailPage — displays full card information with SEO metadata.
 *
 * Features:
 * - Fetches card by slug from URL params
 * - SEO: title, description, canonical URL, og:type article
 * - Category badges
 * - Board/Column breadcrumb navigation
 * - Created/Updated dates
 * - Edit button that opens an inline edit modal
 * - Back navigation to the parent board
 */
const CardDetailPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const [card, setCard] = useState<CardDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [editModalOpen, setEditModalOpen] = useState<boolean>(false);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [saving, setSaving] = useState(false);

  const fetchCard = useCallback(async (): Promise<void> => {
    if (!slug) return;
    try {
      setLoading(true);
      const response = await fetch(`/api/cards/${slug}`);
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Card not found.');
        }
        throw new Error(`Failed to load card (HTTP ${response.status})`);
      }
      const data: CardDetail = await response.json();
      setCard(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  }, [slug]);

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      await fetchCard();
      if (cancelled) return;
    };

    void load();
    return () => { cancelled = true; };
  }, [fetchCard]);

  const openEditModal = () => {
    if (!card) return;
    setEditTitle(card.title);
    setEditDescription(card.description ?? '');
    setEditModalOpen(true);
  };

  const closeEditModal = () => {
    setEditModalOpen(false);
  };

  const handleSave = async () => {
    if (!card) return;
    setSaving(true);
    try {
      const response = await fetch(`/api/cards/${card.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: editTitle,
          description: editDescription,
          column_id: card.column_id,
        }),
      });
      if (!response.ok) {
        throw new Error(`Failed to update card (HTTP ${response.status})`);
      }
      const updated: CardDetail = await response.json();
      setCard(updated);
      setEditModalOpen(false);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Save failed.');
    } finally {
      setSaving(false);
    }
  };

  const pageTitle = card?.meta_title ?? (card ? `${card.title} — Kanban Board` : 'Card — Kanban Board');
  const pageDescription =
    card?.meta_description ??
    (card?.description ?? 'View card details, description, and associated categories.');
  const canonicalUrl = slug ? `${window.location.origin}/cards/${slug}` : undefined;
  const boardSlug = card?.board?.slug;
  const boardTitle = card?.board?.title;
  const columnTitle = card?.column?.title;

  return (
    <>
      <Helmet>
        <title>{pageTitle}</title>
        <meta name="description" content={pageDescription} />
        <meta property="og:title" content={pageTitle} />
        <meta property="og:description" content={pageDescription} />
        <meta property="og:type" content="article" />
        {canonicalUrl && <link rel="canonical" href={canonicalUrl} />}
        {canonicalUrl && <meta property="og:url" content={canonicalUrl} />}
      </Helmet>

      <div className="card-detail-page" style={{ maxWidth: '48rem', margin: '0 auto', padding: '2rem 1rem' }}>
        {loading && (
          <p className="card-detail-page__loading" role="status">
            Loading card…
          </p>
        )}

        {error && (
          <div className="card-detail-page__error">
            <p role="alert" style={{ color: '#e53e3e' }}>{error}</p>
            <Link to="/" style={{ color: '#3182ce', textDecoration: 'none' }}>← Back to boards</Link>
          </div>
        )}

        {!loading && !error && card && (
          <>
            {/* Breadcrumb */}
            <nav className="card-detail-page__breadcrumb" style={{ fontSize: '0.875rem', marginBottom: '1rem', color: '#718096' }}>
              <Link to="/" style={{ color: '#3182ce', textDecoration: 'none' }}>Boards</Link>
              {boardSlug && boardTitle && (
                <>
                  <span style={{ margin: '0 0.375rem' }}>/</span>
                  <Link to={`/boards/${boardSlug}`} style={{ color: '#3182ce', textDecoration: 'none' }}>{boardTitle}</Link>
                </>
              )}
              {columnTitle && (
                <>
                  <span style={{ margin: '0 0.375rem' }}>/</span>
                  <span>{columnTitle}</span>
                </>
              )}
              <span style={{ margin: '0 0.375rem' }}>/</span>
              <span style={{ color: '#2d3748' }}>{card.title}</span>
            </nav>

            {/* Header */}
            <div className="card-detail-page__header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.5rem' }}>
              <div>
                <Link
                  to={boardSlug ? `/boards/${boardSlug}` : '/'}
                  style={{ color: '#3182ce', textDecoration: 'none', fontSize: '0.875rem', display: 'inline-block', marginBottom: '0.75rem' }}
                >
                  ← Back to {boardTitle ?? 'boards'}
                </Link>
                <h1 style={{ fontSize: '1.75rem', margin: 0, color: '#1a202c' }}>{card.title}</h1>
              </div>
              <button
                type="button"
                onClick={openEditModal}
                style={{
                  padding: '0.5rem 1.25rem',
                  backgroundColor: '#3182ce',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '0.875rem',
                  fontWeight: 600,
                  whiteSpace: 'nowrap',
                  marginTop: '1.5rem',
                }}
              >
                ✏️ Edit
              </button>
            </div>

            {/* Category Badges */}
            {card.categories.length > 0 && (
              <div className="card-detail-page__categories" style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '1.5rem' }}>
                {card.categories.map((cat) => (
                  <Link
                    key={cat.id}
                    to={`/categories/${cat.slug}`}
                    style={{
                      display: 'inline-block',
                      padding: '0.25rem 0.75rem',
                      backgroundColor: '#ebf4ff',
                      color: '#2b6cb0',
                      borderRadius: '9999px',
                      fontSize: '0.8125rem',
                      fontWeight: 500,
                      textDecoration: 'none',
                      border: '1px solid #bee3f8',
                    }}
                  >
                    {cat.name}
                  </Link>
                ))}
              </div>
            )}

            {/* Description */}
            {card.description && (
              <div
                className="card-detail-page__description"
                style={{
                  backgroundColor: '#f7fafc',
                  padding: '1.25rem',
                  borderRadius: '8px',
                  marginBottom: '1.5rem',
                  lineHeight: 1.7,
                  color: '#2d3748',
                  whiteSpace: 'pre-wrap',
                }}
              >
                {card.description}
              </div>
            )}

            {!card.description && (
              <div
                className="card-detail-page__description card-detail-page__description--empty"
                style={{
                  backgroundColor: '#f7fafc',
                  padding: '1.25rem',
                  borderRadius: '8px',
                  marginBottom: '1.5rem',
                  color: '#a0aec0',
                  fontStyle: 'italic',
                }}
              >
                No description provided.
              </div>
            )}

            {/* Metadata / Dates */}
            <div
              className="card-detail-page__meta"
              style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: '1rem',
                padding: '1rem',
                backgroundColor: '#fff',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                fontSize: '0.875rem',
                color: '#4a5568',
              }}
            >
              <div>
                <span style={{ fontWeight: 600, display: 'block', marginBottom: '0.25rem', color: '#2d3748' }}>Created</span>
                <time dateTime={card.created_at}>{formatDate(card.created_at)}</time>
              </div>
              <div>
                <span style={{ fontWeight: 600, display: 'block', marginBottom: '0.25rem', color: '#2d3748' }}>Last Updated</span>
                <time dateTime={card.updated_at}>{formatDate(card.updated_at)}</time>
              </div>
            </div>
          </>
        )}

        {/* Edit Modal */}
        {editModalOpen && (
          <div
            className="card-detail-page__modal-overlay"
            role="dialog"
            aria-modal="true"
            aria-label="Edit card"
            onClick={(e) => { if (e.target === e.currentTarget) closeEditModal(); }}
            style={{
              position: 'fixed',
              inset: 0,
              backgroundColor: 'rgba(0,0,0,0.45)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 1000,
            }}
          >
            <div
              className="card-detail-page__modal"
              style={{
                backgroundColor: '#fff',
                borderRadius: '12px',
                padding: '2rem',
                width: '100%',
                maxWidth: '32rem',
                boxShadow: '0 20px 60px rgba(0,0,0,0.15)',
              }}
            >
              <h2 style={{ margin: '0 0 1.25rem', fontSize: '1.25rem' }}>Edit Card</h2>
              <label style={{ display: 'block', marginBottom: '1rem' }}>
                <span style={{ fontWeight: 600, display: 'block', marginBottom: '0.25rem', fontSize: '0.875rem' }}>Title</span>
                <input
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.5rem 0.75rem',
                    border: '1px solid #cbd5e0',
                    borderRadius: '6px',
                    fontSize: '1rem',
                    boxSizing: 'border-box',
                  }}
                />
              </label>
              <label style={{ display: 'block', marginBottom: '1.5rem' }}>
                <span style={{ fontWeight: 600, display: 'block', marginBottom: '0.25rem', fontSize: '0.875rem' }}>Description</span>
                <textarea
                  value={editDescription}
                  onChange={(e) => setEditDescription(e.target.value)}
                  rows={5}
                  style={{
                    width: '100%',
                    padding: '0.5rem 0.75rem',
                    border: '1px solid #cbd5e0',
                    borderRadius: '6px',
                    fontSize: '1rem',
                    resize: 'vertical',
                    boxSizing: 'border-box',
                  }}
                />
              </label>
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
                <button
                  type="button"
                  onClick={closeEditModal}
                  disabled={saving}
                  style={{
                    padding: '0.5rem 1rem',
                    backgroundColor: '#edf2f7',
                    border: '1px solid #cbd5e0',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontSize: '0.875rem',
                  }}
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleSave}
                  disabled={saving || !editTitle.trim()}
                  style={{
                    padding: '0.5rem 1.25rem',
                    backgroundColor: saving ? '#a0aec0' : '#3182ce',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '6px',
                    cursor: saving ? 'not-allowed' : 'pointer',
                    fontSize: '0.875rem',
                    fontWeight: 600,
                  }}
                >
                  {saving ? 'Saving…' : 'Save'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default CardDetailPage;
