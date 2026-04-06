import React, { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { useParams, Link } from 'react-router-dom';

/**
 * Shape of a Category associated with a card.
 */
interface Category {
  id: number;
  name: string;
  slug: string;
}

/**
 * Shape of a Card returned from the API.
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
}

/**
 * Card detail page component.
 *
 * Fetches a single card by its slug from the URL parameter and
 * renders its full details including description and categories.
 */
const CardDetailPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const [card, setCard] = useState<CardDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const fetchCard = async (): Promise<void> => {
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
        if (!cancelled) {
          setCard(data);
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

    void fetchCard();

    return () => {
      cancelled = true;
    };
  }, [slug]);

  const pageTitle = card?.meta_title ?? (card ? `${card.title} — Kanban Board` : 'Card — Kanban Board');
  const pageDescription =
    card?.meta_description ??
    (card?.description ?? 'View card details, description, and associated categories.');

  return (
    <>
      <Helmet>
        <title>{pageTitle}</title>
        <meta name="description" content={pageDescription} />
        <meta property="og:title" content={pageTitle} />
        <meta property="og:description" content={pageDescription} />
        {slug && <link rel="canonical" href={`${window.location.origin}/cards/${slug}`} />}
      </Helmet>

      <div className="card-detail-page">
        {loading && (
          <p className="card-detail-page__loading" role="status">
            Loading card…
          </p>
        )}

        {error && (
          <div className="card-detail-page__error">
            <p role="alert" style={{ color: '#e53e3e' }}>
              {error}
            </p>
            <Link to="/">← Back to boards</Link>
          </div>
        )}

        {!loading && !error && card && (
          <>
            <div
              className="card-detail-page__header"
              style={{ marginBottom: '1.5rem' }}
            >
              <Link
                to="/"
                style={{
                  color: '#3182ce',
                  textDecoration: 'none',
                  fontSize: '0.875rem',
                  display: 'inline-block',
                  marginBottom: '0.75rem',
                }}
              >
                ← Back to boards
              </Link>
              <h1 style={{ fontSize: '1.5rem', margin: 0 }}>{card.title}</h1>
            </div>

            {card.description && (
              <div
                className="card-detail-page__description"
                style={{
                  backgroundColor: '#f7fafc',
                  padding: '1.25rem',
                  borderRadius: '8px',
                  marginBottom: '1.5rem',
                  lineHeight: 1.6,
                }}
              >
                <h2 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>Description</h2>
                <p style={{ margin: 0, color: '#4a5568' }}>{card.description}</p>
              </div>
            )}

            {card.categories.length > 0 && (
              <div className="card-detail-page__categories">
                <h2 style={{ fontSize: '1rem', marginBottom: '0.75rem' }}>Categories</h2>
                <ul
                  style={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    gap: '0.5rem',
                    listStyle: 'none',
                    padding: 0,
                    margin: 0,
                  }}
                >
                  {card.categories.map((category) => (
                    <li key={category.id}>
                      <Link
                        to={`/categories/${category.slug}`}
                        style={{
                          display: 'inline-block',
                          padding: '0.25rem 0.75rem',
                          backgroundColor: '#ebf8ff',
                          color: '#2b6cb0',
                          borderRadius: '9999px',
                          fontSize: '0.8125rem',
                          textDecoration: 'none',
                        }}
                      >
                        {category.name}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div
              className="card-detail-page__meta"
              style={{
                marginTop: '2rem',
                fontSize: '0.8125rem',
                color: '#a0aec0',
              }}
            >
              <p style={{ margin: '0.25rem 0' }}>
                Created: {new Date(card.created_at).toLocaleDateString()}
              </p>
              <p style={{ margin: '0.25rem 0' }}>
                Updated: {new Date(card.updated_at).toLocaleDateString()}
              </p>
            </div>
          </>
        )}
      </div>
    </>
  );
};

export default CardDetailPage;
