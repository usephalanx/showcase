import React, { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { useParams, Link } from 'react-router-dom';

/**
 * Shape of a Card returned when listing by category.
 */
interface Card {
  id: number;
  title: string;
  slug: string;
  description: string | null;
}

/**
 * Shape of a Category returned from the API.
 */
interface CategoryDetail {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  meta_title: string | null;
  meta_description: string | null;
  parent_id: number | null;
  cards: Card[];
}

/**
 * Category page component (filtered view).
 *
 * Fetches a single category by its slug from the URL parameter and
 * renders the list of cards associated with that category.
 */
const CategoryPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const [category, setCategory] = useState<CategoryDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const fetchCategory = async (): Promise<void> => {
      if (!slug) return;
      try {
        setLoading(true);
        const response = await fetch(`/api/categories/${slug}`);
        if (!response.ok) {
          if (response.status === 404) {
            throw new Error('Category not found.');
          }
          throw new Error(`Failed to load category (HTTP ${response.status})`);
        }
        const data: CategoryDetail = await response.json();
        if (!cancelled) {
          setCategory(data);
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

    void fetchCategory();

    return () => {
      cancelled = true;
    };
  }, [slug]);

  const pageTitle =
    category?.meta_title ?? (category ? `${category.name} — Kanban Board` : 'Category — Kanban Board');
  const pageDescription =
    category?.meta_description ??
    (category?.description ?? 'Browse cards filtered by category.');

  return (
    <>
      <Helmet>
        <title>{pageTitle}</title>
        <meta name="description" content={pageDescription} />
        <meta property="og:title" content={pageTitle} />
        <meta property="og:description" content={pageDescription} />
        {slug && <link rel="canonical" href={`${window.location.origin}/categories/${slug}`} />}
      </Helmet>

      <div className="category-page">
        {loading && (
          <p className="category-page__loading" role="status">
            Loading category…
          </p>
        )}

        {error && (
          <div className="category-page__error">
            <p role="alert" style={{ color: '#e53e3e' }}>
              {error}
            </p>
            <Link to="/">← Back to boards</Link>
          </div>
        )}

        {!loading && !error && category && (
          <>
            <div
              className="category-page__header"
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
              <h1 style={{ fontSize: '1.5rem', margin: 0 }}>{category.name}</h1>
              {category.description && (
                <p style={{ color: '#718096', marginTop: '0.5rem' }}>{category.description}</p>
              )}
            </div>

            {category.cards.length === 0 ? (
              <div className="category-page__empty">
                <p>No cards in this category yet.</p>
              </div>
            ) : (
              <ul
                className="category-page__card-list"
                style={{
                  listStyle: 'none',
                  padding: 0,
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
                  gap: '1rem',
                }}
              >
                {category.cards.map((card) => (
                  <li key={card.id}>
                    <Link
                      to={`/cards/${card.slug}`}
                      style={{
                        display: 'block',
                        padding: '1rem',
                        border: '1px solid #e2e8f0',
                        borderRadius: '8px',
                        textDecoration: 'none',
                        color: 'inherit',
                      }}
                      aria-label={`View card: ${card.title}`}
                    >
                      <h2 style={{ fontSize: '1rem', margin: '0 0 0.5rem' }}>{card.title}</h2>
                      {card.description && (
                        <p
                          style={{
                            margin: 0,
                            color: '#718096',
                            fontSize: '0.875rem',
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                          }}
                        >
                          {card.description}
                        </p>
                      )}
                    </Link>
                  </li>
                ))}
              </ul>
            )}
          </>
        )}
      </div>
    </>
  );
};

export default CategoryPage;
