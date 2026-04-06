import React from 'react';
import { Helmet } from 'react-helmet-async';
import { Link } from 'react-router-dom';

/**
 * 404 Not Found page component.
 *
 * Rendered when no route matches the current URL. Provides
 * a user-friendly message and a link back to the home page.
 */
const NotFoundPage: React.FC = () => {
  return (
    <>
      <Helmet>
        <title>Page Not Found — Kanban Board</title>
        <meta name="description" content="The page you are looking for does not exist." />
        <meta name="robots" content="noindex, nofollow" />
      </Helmet>

      <div
        className="not-found-page"
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '50vh',
          textAlign: 'center',
        }}
      >
        <h1 style={{ fontSize: '3rem', color: '#e53e3e', margin: '0 0 0.5rem' }}>404</h1>
        <p style={{ fontSize: '1.25rem', color: '#4a5568', marginBottom: '1.5rem' }}>
          The page you&apos;re looking for doesn&apos;t exist.
        </p>
        <Link
          to="/"
          style={{
            color: '#3182ce',
            textDecoration: 'none',
            fontWeight: 600,
          }}
        >
          ← Go back to home
        </Link>
      </div>
    </>
  );
};

export default NotFoundPage;
