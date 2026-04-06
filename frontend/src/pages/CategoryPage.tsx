import React, { useEffect, useState, useMemo } from 'react';
import { Helmet } from 'react-helmet-async';
import { useParams, Link } from 'react-router-dom';

/* ------------------------------------------------------------------ */
/*  Type definitions                                                   */
/* ------------------------------------------------------------------ */

interface Card {
  id: number;
  title: string;
  slug: string;
  description: string | null;
}

interface CategorySummary {
  id: number;
  name: string;
  slug: string;
}

interface CategoryDetail {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  meta_title: string | null;
  meta_description: string | null;
  parent_id: number | null;
  parent: CategorySummary | null;
  children: CategorySummary[];
  cards: Card[];
}

interface BreadcrumbItem {
  name: string;
  slug: string;
}

/* ------------------------------------------------------------------ */
/*  Sub-components (page-level only, kept minimal)                     */
/* ------------------------------------------------------------------ */

const SEOHead: React.FC<{
  title: string;
  description: string;
  canonicalPath: string;
}> = ({ title, description, canonicalPath }) => (
  <Helmet>
    <title>{title}</title>
    <meta name="description" content={description} />
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:type" content="website" />
    <link rel="canonical" href={`${window.location.origin}${canonicalPath}`} />
    <script type="application/ld+json">
      {JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        name: title,
        description,
        url: `${window.location.origin}${canonicalPath}`,
      })}
    </script>
  </Helmet>
);

const Breadcrumb: React.FC<{ items: BreadcrumbItem[] }> = ({ items }) => (
  <nav aria-label="Breadcrumb" style={{ marginBottom: '1rem', fontSize: '0.875rem' }}>
    <ol
      style={{
        listStyle: 'none',
        display: 'flex',
        flexWrap: 'wrap',
        gap: '0.25rem',
        padding: 0,
        margin: 0,
      }}
    >
      <li>
        <Link to="/" style={{ color: '#3182ce', textDecoration: 'none' }}>Home</Link>
        <span style={{ margin: '0 0.35rem', color: '#a0aec0' }}>/</span>
      </li>
      <li>
        <Link to="/categories" style={{ color: '#3182ce', textDecoration: 'none' }}>Categories</Link>
        {items.length > 0 && <span style={{ margin: '0 0.35rem', color: '#a0aec0' }}>/</span>}
      </li>
      {items.map((item, idx) => {
        const isLast = idx === items.length - 1;
        return (
          <li key={item.slug} aria-current={isLast ? 'page' : undefined}>
            {isLast ? (
              <span style={{ color: '#4a5568', fontWeight: 600 }}>{item.name}</span>
            ) : (
              <>
                <Link
                  to={`/categories/${item.slug}`}
                  style={{ color: '#3182ce', textDecoration: 'none' }}
                >
                  {item.name}
                </Link>
                <span style={{ margin: '0 0.35rem', color: '#a0aec0' }}>/</span>
              </>
            )}
          </li>
        );
      })}
    </ol>
  </nav>
);

const CategorySidebar: React.FC<{
  currentSlug: string;
  parent: CategorySummary | null;
  children: CategorySummary[];
}> = ({ currentSlug, parent, children }) => (
  <aside
    className="category-sidebar"
    style={{
      minWidth: 200,
      maxWidth: 260,
      borderRight: '1px solid #e2e8f0',
      paddingRight: '1rem',
    }}
  >
    <h2 style={{ fontSize: '1rem', marginTop: 0, marginBottom: '0.75rem', color: '#2d3748' }}>
      Categories
    </h2>
    {parent && (
      <div style={{ marginBottom: '0.75rem' }}>
        <span style={{ fontSize: '0.75rem', color: '#a0aec0', textTransform: 'uppercase' }}>
          Parent
        </span>
        <Link
          to={`/categories/${parent.slug}`}
          style={{
            display: 'block',
            padding: '0.35rem 0.5rem',
            color: '#3182ce',
            textDecoration: 'none',
            borderRadius: 4,
            fontSize: '0.875rem',
          }}
        >
          ↑ {parent.name}
        </Link>
      </div>
    )}
    {children.length > 0 && (
      <div>
        <span style={{ fontSize: '0.75rem', color: '#a0aec0', textTransform: 'uppercase' }}>
          Subcategories
        </span>
        <ul style={{ listStyle: 'none', padding: 0, margin: '0.25rem 0 0 0' }}>
          {children.map((child) => (
            <li key={child.id}>
              <Link
                to={`/categories/${child.slug}`}
                style={{
                  display: 'block',
                  padding: '0.35rem 0.5rem',
                  color: child.slug === currentSlug ? '#2d3748' : '#3182ce',
                  fontWeight: child.slug === currentSlug ? 600 : 400,
                  textDecoration: 'none',
                  borderRadius: 4,
                  backgroundColor: child.slug === currentSlug ? '#ebf8ff' : 'transparent',
                  fontSize: '0.875rem',
                }}
              >
                {child.name}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    )}
    {!parent && children.length === 0 && (
      <p style={{ fontSize: '0.875rem', color: '#a0aec0' }}>No related categories.</p>
    )}
  </aside>
);

const KanbanCard: React.FC<{ card: Card }> = ({ card }) => (
  <article
    className="kanban-card"
    style={{
      border: '1px solid #e2e8f0',
      borderRadius: 8,
      padding: '1rem',
      backgroundColor: '#fff',
      boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
      transition: 'box-shadow 0.15s ease',
    }}
  >
    <h3 style={{ fontSize: '1rem', margin: '0 0 0.5rem 0' }}>
      <Link
        to={`/cards/${card.slug}`}
        style={{ color: '#2d3748', textDecoration: 'none' }}
      >
        {card.title}
      </Link>
    </h3>
    {card.description && (
      <p style={{ margin: 0, fontSize: '0.875rem', color: '#718096', lineHeight: 1.5 }}>
        {card.description.length > 120
          ? `${card.description.slice(0, 120)}…`
          : card.description}
      </p>
    )}
  </article>
);

/* ------------------------------------------------------------------ */
/*  Main page component                                                */
/* ------------------------------------------------------------------ */

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
        setError(null);
        const response = await fetch(`/api/categories/${slug}`);
        if (!response.ok) {
          if (response.status === 404) throw new Error('Category not found.');
          throw new Error(`Failed to load category (HTTP ${response.status})`);
        }
        const data: CategoryDetail = await response.json();
        if (!cancelled) {
          setCategory(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'An unexpected error occurred.');
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    void fetchCategory();
    return () => { cancelled = true; };
  }, [slug]);

  /* Build breadcrumb trail */
  const breadcrumbItems: BreadcrumbItem[] = useMemo(() => {
    if (!category) return [];
    const trail: BreadcrumbItem[] = [];
    if (category.parent) {
      trail.push({ name: category.parent.name, slug: category.parent.slug });
    }
    trail.push({ name: category.name, slug: category.slug });
    return trail;
  }, [category]);

  /* SEO values */
  const pageTitle =
    category?.meta_title ??
    (category ? `${category.name} — Kanban Board` : 'Category — Kanban Board');
  const pageDescription =
    category?.meta_description ??
    category?.description ??
    'Browse cards filtered by category.';
  const canonicalPath = `/categories/${slug ?? ''}`;

  /* ---- Render ---- */

  if (loading) {
    return (
      <>
        <SEOHead title={pageTitle} description={pageDescription} canonicalPath={canonicalPath} />
        <div className="category-page" style={{ padding: '2rem' }}>
          <p role="status">Loading category…</p>
        </div>
      </>
    );
  }

  if (error || !category) {
    return (
      <>
        <SEOHead title="Error — Kanban Board" description="Category could not be loaded." canonicalPath={canonicalPath} />
        <div className="category-page" style={{ padding: '2rem' }}>
          <p role="alert" style={{ color: '#e53e3e' }}>{error ?? 'Category not found.'}</p>
          <Link to="/" style={{ color: '#3182ce' }}>← Back to boards</Link>
        </div>
      </>
    );
  }

  return (
    <>
      <SEOHead title={pageTitle} description={pageDescription} canonicalPath={canonicalPath} />

      <div className="category-page" style={{ padding: '2rem', maxWidth: 1200, margin: '0 auto' }}>
        <Breadcrumb items={breadcrumbItems} />

        <h1 style={{ fontSize: '1.5rem', margin: '0 0 0.25rem 0' }}>{category.name}</h1>
        {category.description && (
          <p style={{ color: '#718096', marginTop: '0.25rem', marginBottom: '1.5rem' }}>
            {category.description}
          </p>
        )}

        <div
          className="category-page__layout"
          style={{
            display: 'flex',
            gap: '1.5rem',
            alignItems: 'flex-start',
            flexWrap: 'wrap',
          }}
        >
          <CategorySidebar
            currentSlug={category.slug}
            parent={category.parent}
            children={category.children}
          />

          <main style={{ flex: 1, minWidth: 280 }}>
            {category.cards.length === 0 ? (
              <p style={{ color: '#a0aec0' }}>No cards in this category yet.</p>
            ) : (
              <div
                className="category-page__grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))',
                  gap: '1rem',
                }}
              >
                {category.cards.map((card) => (
                  <KanbanCard key={card.id} card={card} />
                ))}
              </div>
            )}
          </main>
        </div>
      </div>
    </>
  );
};

export default CategoryPage;
