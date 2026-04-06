import { render, waitFor } from "@testing-library/react";
import { HelmetProvider } from "react-helmet-async";
import { describe, it, expect } from "vitest";
import SEOHead, { type SEOHeadProps } from "./SEOHead";

/**
 * Helper to render SEOHead within the required HelmetProvider context
 * and return a reference to the HelmetProvider's internal data for assertions.
 */
function renderSEOHead(props: SEOHeadProps) {
  const helmetContext: { helmet?: any } = {};
  const result = render(
    <HelmetProvider context={helmetContext}>
      <SEOHead {...props} />
    </HelmetProvider>,
  );
  return { ...result, helmetContext };
}

describe("SEOHead", () => {
  it("renders without crashing", () => {
    const { helmetContext } = renderSEOHead({
      title: "Home",
      description: "Welcome to the Kanban board.",
    });
    expect(helmetContext.helmet).toBeDefined();
  });

  it("prepends the default site name to the title", async () => {
    const { helmetContext } = renderSEOHead({
      title: "Dashboard",
      description: "Your dashboard.",
    });

    await waitFor(() => {
      const titleTag = helmetContext.helmet?.title?.toString() ?? "";
      expect(titleTag).toContain("KanbanBoard | Dashboard");
    });
  });

  it("prepends a custom site name when provided", async () => {
    const { helmetContext } = renderSEOHead({
      title: "Tasks",
      description: "All tasks.",
      siteName: "MySite",
    });

    await waitFor(() => {
      const titleTag = helmetContext.helmet?.title?.toString() ?? "";
      expect(titleTag).toContain("MySite | Tasks");
    });
  });

  it("sets the meta description", async () => {
    const { helmetContext } = renderSEOHead({
      title: "About",
      description: "About this application.",
    });

    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('content="About this application."');
    });
  });

  it("sets og:title with the full title", async () => {
    const { helmetContext } = renderSEOHead({
      title: "Board View",
      description: "View a board.",
    });

    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('property="og:title"');
      expect(metaTags).toContain("KanbanBoard | Board View");
    });
  });

  it("sets og:description", async () => {
    const { helmetContext } = renderSEOHead({
      title: "Cards",
      description: "All your cards in one place.",
    });

    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('property="og:description"');
      expect(metaTags).toContain("All your cards in one place.");
    });
  });

  it("defaults og:type to 'website'", async () => {
    const { helmetContext } = renderSEOHead({
      title: "Home",
      description: "Homepage.",
    });

    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('property="og:type"');
      expect(metaTags).toContain('content="website"');
    });
  });

  it("allows overriding og:type", async () => {
    const { helmetContext } = renderSEOHead({
      title: "Article",
      description: "An article.",
      ogType: "article",
    });

    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('content="article"');
    });
  });

  it("renders a canonical link when canonicalUrl is provided", async () => {
    const { helmetContext } = renderSEOHead({
      title: "Page",
      description: "A page.",
      canonicalUrl: "https://example.com/page",
    });

    await waitFor(() => {
      const linkTags = helmetContext.helmet?.link?.toString() ?? "";
      expect(linkTags).toContain('rel="canonical"');
      expect(linkTags).toContain('href="https://example.com/page"');
    });
  });

  it("does not render a canonical link when canonicalUrl is omitted", async () => {
    const { helmetContext } = renderSEOHead({
      title: "No Canonical",
      description: "No canonical URL.",
    });

    await waitFor(() => {
      const linkTags = helmetContext.helmet?.link?.toString() ?? "";
      expect(linkTags).not.toContain('rel="canonical"');
    });
  });
});
