import { Helmet } from 'react-helmet-async';

/**
 * Tag list page component.
 * Displays all available tags used to categorize cards across boards.
 */
function TagListPage(): JSX.Element {
  return (
    <>
      <Helmet>
        <title>Tags — Kanban Board</title>
        <meta
          name="description"
          content="Browse all tags used to categorize and filter tasks across your Kanban boards."
        />
        <link rel="canonical" href="/tags" />
      </Helmet>
      <main className="p-6">
        <h1 className="text-3xl font-bold text-primary-600 mb-4">
          Tags
        </h1>
        <p className="text-surface-500">
          Your tags will appear here.
        </p>
      </main>
    </>
  );
}

export default TagListPage;
