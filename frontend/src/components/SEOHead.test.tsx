import { describe, it, expect } from "vitest";
import { render, waitFor } from "@testing-library/react";
import { HelmetProvider } from "react-helmet-async";
import SEOHead, { SEOHeadProps } from "./SEOHead";

/**
 * Helper to render SEOHead within a HelmetProvider and return the
 * helmet context so we can inspect rendered tags.
 */
function renderSEOHead(props: SEOHeadProps) {
  const helmetContext: { helmet?: Record<string, any> } = {};
  const result = render(
    <HelmetProvider context={helmetContext}>
      <SEOHead {...props} />
    </HelmetProvider>
  );
  return { ...result, helmetContext };
}

const defaultProps: SEOHeadProps = {
  title: "Test Board - Kanban App",
  description: "A test board for organizing tasks efficiently.",
  url: "https://example.com/boards/test-board",
};

describe("SEOHead", () => {
  it("renders without crashing", () => {
    const { helmetContext } = renderSEOHead(defaultProps);
    expect(helmetContext.helmet).toBeDefined();
  });

  it("renders the correct <title>", async () => {
    const { helmetContext } = renderSEOHead(defaultProps);
    await waitFor(() => {
      const titleTag = helmetContext.helmet?.title?.toString() ?? "";
      expect(titleTag).toContain("Test Board - Kanban App");
    });
  });

  it("renders meta description", async () => {
    const { helmetContext } = renderSEOHead(defaultProps);
    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('name="description"');
      expect(metaTags).toContain(
        "A test board for organizing tasks efficiently."
      );
    });
  });

  it("renders og:title meta tag", async () => {
    const { helmetContext } = renderSEOHead(defaultProps);
    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('property="og:title"');
      expect(metaTags).toContain("Test Board - Kanban App");
    });
  });

  it("renders og:description meta tag", async () => {
    const { helmetContext } = renderSEOHead(defaultProps);
    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('property="og:description"');
      expect(metaTags).toContain(
        "A test board for organizing tasks efficiently."
      );
    });
  });

  it("renders og:url meta tag with the provided url", async () => {
    const { helmetContext } = renderSEOHead(defaultProps);
    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('property="og:url"');
      expect(metaTags).toContain("https://example.com/boards/test-board");
    });
  });

  it("renders og:type as website", async () => {
    const { helmetContext } = renderSEOHead(defaultProps);
    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('property="og:type"');
      expect(metaTags).toContain("website");
    });
  });

  it("renders canonical link with the provided url", async () => {
    const { helmetContext } = renderSEOHead(defaultProps);
    await waitFor(() => {
      const linkTags = helmetContext.helmet?.link?.toString() ?? "";
      expect(linkTags).toContain('rel="canonical"');
      expect(linkTags).toContain("https://example.com/boards/test-board");
    });
  });

  it("renders twitter:card as 'summary' when no ogImage is provided", async () => {
    const { helmetContext } = renderSEOHead(defaultProps);
    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('name="twitter:card"');
      expect(metaTags).toContain('content="summary"');
    });
  });

  it("renders twitter:title meta tag", async () => {
    const { helmetContext } = renderSEOHead(defaultProps);
    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('name="twitter:title"');
      expect(metaTags).toContain("Test Board - Kanban App");
    });
  });

  it("renders twitter:description meta tag", async () => {
    const { helmetContext } = renderSEOHead(defaultProps);
    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('name="twitter:description"');
      expect(metaTags).toContain(
        "A test board for organizing tasks efficiently."
      );
    });
  });

  it("does NOT render og:image when ogImage prop is not provided", async () => {
    const { helmetContext } = renderSEOHead(defaultProps);
    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).not.toContain('property="og:image"');
    });
  });

  it("does NOT render twitter:image when ogImage prop is not provided", async () => {
    const { helmetContext } = renderSEOHead(defaultProps);
    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).not.toContain('name="twitter:image"');
    });
  });

  it("renders og:image when ogImage prop IS provided", async () => {
    const propsWithImage: SEOHeadProps = {
      ...defaultProps,
      ogImage: "https://example.com/images/board-preview.png",
    };
    const { helmetContext } = renderSEOHead(propsWithImage);
    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('property="og:image"');
      expect(metaTags).toContain(
        "https://example.com/images/board-preview.png"
      );
    });
  });

  it("renders twitter:image when ogImage prop IS provided", async () => {
    const propsWithImage: SEOHeadProps = {
      ...defaultProps,
      ogImage: "https://example.com/images/board-preview.png",
    };
    const { helmetContext } = renderSEOHead(propsWithImage);
    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('name="twitter:image"');
      expect(metaTags).toContain(
        "https://example.com/images/board-preview.png"
      );
    });
  });

  it("renders twitter:card as 'summary_large_image' when ogImage is provided", async () => {
    const propsWithImage: SEOHeadProps = {
      ...defaultProps,
      ogImage: "https://example.com/images/board-preview.png",
    };
    const { helmetContext } = renderSEOHead(propsWithImage);
    await waitFor(() => {
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain('content="summary_large_image"');
    });
  });

  it("updates tags when props change", async () => {
    const helmetContext: { helmet?: Record<string, any> } = {};
    const { rerender } = render(
      <HelmetProvider context={helmetContext}>
        <SEOHead {...defaultProps} />
      </HelmetProvider>
    );

    const updatedProps: SEOHeadProps = {
      title: "Updated Title",
      description: "Updated description for the page.",
      url: "https://example.com/boards/updated-board",
    };

    rerender(
      <HelmetProvider context={helmetContext}>
        <SEOHead {...updatedProps} />
      </HelmetProvider>
    );

    await waitFor(() => {
      const titleTag = helmetContext.helmet?.title?.toString() ?? "";
      expect(titleTag).toContain("Updated Title");
      const metaTags = helmetContext.helmet?.meta?.toString() ?? "";
      expect(metaTags).toContain("Updated description for the page.");
      const linkTags = helmetContext.helmet?.link?.toString() ?? "";
      expect(linkTags).toContain("https://example.com/boards/updated-board");
    });
  });
});
