/**
 * SEOHead – A reusable component for managing document <head> meta tags.
 *
 * Uses react-helmet-async to inject:
 * - <title> (with site name prepended)
 * - <meta name="description">
 * - <meta property="og:title">
 * - <meta property="og:description">
 * - <meta property="og:type">
 * - <link rel="canonical">
 */

import { Helmet } from "react-helmet-async";

const SITE_NAME = "KanbanBoard";

export interface SEOHeadProps {
  /** Page-specific title. The site name is automatically prepended. */
  title: string;
  /** Meta description for the page. */
  description: string;
  /** Canonical URL for the page. */
  canonicalUrl?: string;
  /**
   * Open Graph type.
   * @default "website"
   */
  ogType?: string;
  /**
   * Optional override for the site name prepended to the title.
   * Defaults to the built-in SITE_NAME constant.
   */
  siteName?: string;
}

export default function SEOHead({
  title,
  description,
  canonicalUrl,
  ogType = "website",
  siteName,
}: SEOHeadProps) {
  const resolvedSiteName = siteName ?? SITE_NAME;
  const fullTitle = `${resolvedSiteName} | ${title}`;

  return (
    <Helmet>
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      <meta property="og:title" content={fullTitle} />
      <meta property="og:description" content={description} />
      <meta property="og:type" content={ogType} />
      {canonicalUrl && <link rel="canonical" href={canonicalUrl} />}
    </Helmet>
  );
}
