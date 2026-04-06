import { Routes, Route } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import HomePage from './pages/HomePage';
import BoardDetailPage from './pages/BoardDetailPage';
import TagListPage from './pages/TagListPage';
import TagDetailPage from './pages/TagDetailPage';
import NotFoundPage from './pages/NotFoundPage';

/**
 * Root application component.
 * Sets up global meta tags and top-level routing with SEO-friendly slug-based URLs.
 */
function App(): JSX.Element {
  return (
    <>
      <Helmet>
        <title>Kanban Board</title>
        <meta
          name="description"
          content="Organize your tasks and projects with an intuitive drag-and-drop Kanban board."
        />
        <meta name="robots" content="index, follow" />
        <meta property="og:type" content="website" />
        <meta property="og:site_name" content="Kanban Board" />
      </Helmet>
      <div className="min-h-screen bg-surface-50">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/boards/:slug" element={<BoardDetailPage />} />
          <Route path="/tags" element={<TagListPage />} />
          <Route path="/tags/:slug" element={<TagDetailPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
