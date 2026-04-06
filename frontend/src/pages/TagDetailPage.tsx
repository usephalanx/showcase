import { useParams } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';

/**
 * Tag detail page component.
 * Displays all cards associated with a specific tag identified by its slug.
 */
function TagDetailPage(): JSX.Element {
  const { slug } = useParams<{ slug: string }>();

  return (
    <>
      <Helmet>
        <title>{slug ? `${slug} — Tags — Kanban Board` : 'Tag — Kanban Board'}</title>
        <meta
          name="description"
          content={`View all cards tagged with ${slug ?? 'this tag'} across your Kanban boards.`}
        />
        <link rel="canonical" href={`/tags/${slug ?? ''}`} />
      </Helmet>
      <main className="p-6">
        <h1 className="text-3xl font-bold text-primary-600 mb-4">
          Tag: {slug}
        </h1>
        <p className="text-surface-500">
          Cards with this tag will appear here.
        </p>
      </main>
    </>
  );
}

export default TagDetailPage;
