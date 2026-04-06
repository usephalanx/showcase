import React from 'react';
import { Helmet } from 'react-helmet-async';
import { Routes, Route } from 'react-router-dom';

/**
 * Root application component.
 *
 * Sets up default SEO meta tags via React Helmet and defines
 * the top-level route configuration.
 */
const App: React.FC = () => {
  return (
    <>
      <Helmet>
        <title>Kanban Board — Organize Your Projects</title>
        <meta
          name="description"
          content="Organize your projects with drag-and-drop task management, categories, and tags."
        />
        <meta property="og:title" content="Kanban Board — Organize Your Projects" />
        <meta
          property="og:description"
          content="Drag-and-drop task management with categories and tags."
        />
      </Helmet>
      <main>
        <Routes>
          <Route
            path="/"
            element={
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  minHeight: '100vh',
                  fontFamily: 'var(--font-family-sans)',
                }}
              >
                <h1>Kanban Board</h1>
              </div>
            }
          />
        </Routes>
      </main>
    </>
  );
};

export default App;
