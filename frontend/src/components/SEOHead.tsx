/**
 * SEOHead component for managing document head meta tags.
 *
 * Uses react-helmet-async to render SEO-critical tags including:
 * - <title>
 * - <meta name="description">
 * - <meta property="og:title">
 * - <meta property="og:description">
 * - <meta property="og:url">
 * - <meta property="og:image"> (optional)
 * - <meta property="og:type">
 * - <meta name="twitter:card">
 * - <meta name="twitter:title">
 * - <meta name="twitter:description">
 * - <meta name="twitter:image"> (optional)
 * - <link rel="canonical">
 */

import { Helmet } from "react-helmet-async";

/**
 * Props for the SEOHead component.
 */
export interface SEOHeadProps {
  /** The page title rendered in the <title> tag and og:title. */
  title: string;
  /** The meta description (max ~160 chars recommended). */
  description: string;
  /** The canonical URL for this page. Also used for og:url. */
  url: string;
  /** Optional Open Graph / Twitter image URL. */
  ogImage?: string;
}

/**
 * SEOHead renders all essential meta tags for SEO and social sharing.
 *
 * All data is received via props — no internal API calls or routing logic.
 *
 * @example
 * ```tsx
 * <SEOHead
 *   title="My Kanban Board"
 *   description="Organize your tasks with this kanban board."
 *   url="https://example.com/boards/my-kanban-board"
 *   ogImage="https://example.com/images/board-preview.png"
 * />
 * ```
 */
export default function SEOHead({
  title,
  description,
  url,
  ogImage,
}: SEOHeadProps) {
  return (
    <Helmet>
      {/* Primary title */}
      <title>{title}</title>

      {/* Standard meta description */}
      <meta name="description" content={description} />

      {/* Open Graph */}
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:url" content={url} />
      <meta property="og:type" content="website" />
      {ogImage && <meta property="og:image" content={ogImage} />}

      {/* Twitter Card */}
      <meta
        name="twitter:card"
        content={ogImage ? "summary_large_image" : "summary"}
      />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      {ogImage && <meta name="twitter:image" content={ogImage} />}

      {/* Canonical URL */}
      <link rel="canonical" href={url} />
    </Helmet>
  );
}
