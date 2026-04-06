import { useParams } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';

/**
 * Board detail page component.
 * Displays a single kanban board identified by its SEO-friendly slug.
 */
function BoardDetailPage(): JSX.Element {
  const { slug } = useParams<{ slug: string }>();

  return (
    <>
      <Helmet>
        <title>{slug ? `${slug} — Kanban Board` : 'Board — Kanban Board'}</title>
        <meta
          name="description"
          content={`View and manage tasks on the ${slug ?? 'selected'} board.`}
        />
        <link rel="canonical" href={`/boards/${slug ?? ''}`} />
      </Helmet>
      <main className="p-6">
        <h1 className="text-3xl font-bold text-primary-600 mb-4">
          Board: {slug}
        </h1>
        <p className="text-surface-500">
          Board details and columns will appear here.
        </p>
      </main>
    </>
  );
}

export default BoardDetailPage;
