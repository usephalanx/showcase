import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';

/**
 * 404 Not Found page component.
 * Displayed when the user navigates to an invalid or non-existent route.
 */
function NotFoundPage(): JSX.Element {
  return (
    <>
      <Helmet>
        <title>Page Not Found — Kanban Board</title>
        <meta name="description" content="The page you are looking for does not exist." />
        <meta name="robots" content="noindex, nofollow" />
      </Helmet>
      <main className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h1 className="text-6xl font-bold text-surface-300 mb-4">
            404
          </h1>
          <p className="text-xl text-surface-500 mb-6">
            Page not found
          </p>
          <Link
            to="/"
            className="text-primary-600 hover:text-primary-700 underline text-lg"
          >
            Go back home
          </Link>
        </div>
      </main>
    </>
  );
}

export default NotFoundPage;
