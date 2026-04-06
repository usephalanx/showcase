import { Helmet } from 'react-helmet-async';

/**
 * Home page component displaying the list of kanban boards.
 * Serves as the main landing page of the application.
 */
function HomePage(): JSX.Element {
  return (
    <>
      <Helmet>
        <title>Kanban Board — All Boards</title>
        <meta
          name="description"
          content="Browse all your Kanban boards. Organize tasks and projects with an intuitive drag-and-drop interface."
        />
        <link rel="canonical" href="/" />
      </Helmet>
      <main className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-primary-600 mb-4">
            Kanban Board
          </h1>
          <p className="text-surface-500 text-lg">
            Your boards will appear here.
          </p>
        </div>
      </main>
    </>
  );
}

export default HomePage;
