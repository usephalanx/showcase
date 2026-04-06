import { Routes, Route } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';

/**
 * Root application component.
 * Sets up global meta tags and top-level routing.
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
      </Helmet>
      <div className="min-h-screen bg-surface-50">
        <Routes>
          <Route
            path="/"
            element={
              <main className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                  <h1 className="text-4xl font-bold text-primary-600 mb-4">
                    Kanban Board
                  </h1>
                  <p className="text-surface-500 text-lg">
                    Project initialized. Start building!
                  </p>
                </div>
              </main>
            }
          />
        </Routes>
      </div>
    </>
  );
}

export default App;
