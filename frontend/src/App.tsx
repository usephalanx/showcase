import { Routes, Route } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';

/**
 * Root application component.
 *
 * Sets up page-level routes and default SEO meta tags
 * via React Helmet Async.
 */
function App(): JSX.Element {
  return (
    <>
      <Helmet>
        <title>Kanban Board — Organize Your Projects</title>
        <meta
          name="description"
          content="Kanban Board — Organize your projects with drag-and-drop task management, categories, and tags."
        />
      </Helmet>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
    </>
  );
}

/**
 * Minimal home page placeholder.
 *
 * Will be replaced by the full HomePage component
 * in a subsequent task.
 */
function Home(): JSX.Element {
  return (
    <div>
      <h1>Kanban Board</h1>
      <p>Welcome to Kanban Board. Start organizing your projects.</p>
    </div>
  );
}

/**
 * Minimal 404 page placeholder.
 *
 * Will be replaced by the full NotFoundPage component
 * in a subsequent task.
 */
function NotFound(): JSX.Element {
  return (
    <div>
      <Helmet>
        <title>Page Not Found — Kanban Board</title>
      </Helmet>
      <h1>404 — Page Not Found</h1>
      <p>The page you are looking for does not exist.</p>
    </div>
  );
}

export default App;
