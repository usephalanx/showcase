import React from 'react';
import { Helmet } from 'react-helmet-async';
import { Routes, Route } from 'react-router-dom';

import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import BoardPage from './pages/BoardPage';
import CardDetailPage from './pages/CardDetailPage';
import CategoryPage from './pages/CategoryPage';
import NotFoundPage from './pages/NotFoundPage';

/**
 * Root application component.
 *
 * Sets up default SEO meta tags via React Helmet and defines
 * the top-level route configuration with SEO-friendly slug-based URLs.
 *
 * Routes:
 * - /                    HomePage (list boards)
 * - /boards/:slug        BoardPage (kanban view)
 * - /cards/:slug         CardDetailPage (single card detail)
 * - /categories/:slug    CategoryPage (filtered view by category)
 * - *                    NotFoundPage (404 fallback)
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
        <meta property="og:type" content="website" />
        <link rel="canonical" href={window.location.origin} />
      </Helmet>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/boards/:slug" element={<BoardPage />} />
          <Route path="/cards/:slug" element={<CardDetailPage />} />
          <Route path="/categories/:slug" element={<CategoryPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Layout>
    </>
  );
};

export default App;
