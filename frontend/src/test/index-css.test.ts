import { describe, it, expect } from "vitest";
import { readFileSync } from "fs";
import { resolve } from "path";

/**
 * Structural tests for index.css to verify that required CSS variables,
 * selectors, and design tokens are defined.
 */
const cssContent = readFileSync(
  resolve(__dirname, "..", "index.css"),
  "utf-8",
);

describe("index.css", () => {
  describe("CSS custom properties (variables)", () => {
    it("defines color variables", () => {
      expect(cssContent).toContain("--color-white");
      expect(cssContent).toContain("--color-gray-50");
      expect(cssContent).toContain("--color-gray-100");
      expect(cssContent).toContain("--color-gray-200");
      expect(cssContent).toContain("--color-gray-300");
      expect(cssContent).toContain("--color-gray-400");
      expect(cssContent).toContain("--color-gray-500");
      expect(cssContent).toContain("--color-gray-600");
      expect(cssContent).toContain("--color-gray-700");
      expect(cssContent).toContain("--color-gray-800");
      expect(cssContent).toContain("--color-gray-900");
      expect(cssContent).toContain("--color-primary");
      expect(cssContent).toContain("--color-primary-hover");
      expect(cssContent).toContain("--color-danger");
      expect(cssContent).toContain("--color-danger-hover");
      expect(cssContent).toContain("--color-success");
    });

    it("defines spacing variables", () => {
      expect(cssContent).toContain("--space-1");
      expect(cssContent).toContain("--space-2");
      expect(cssContent).toContain("--space-4");
      expect(cssContent).toContain("--space-6");
      expect(cssContent).toContain("--space-8");
    });

    it("defines typography variables", () => {
      expect(cssContent).toContain("--font-family-sans");
      expect(cssContent).toContain("--font-size-base");
      expect(cssContent).toContain("--font-size-sm");
      expect(cssContent).toContain("--font-size-lg");
      expect(cssContent).toContain("--font-weight-normal");
      expect(cssContent).toContain("--font-weight-bold");
      expect(cssContent).toContain("--line-height-normal");
    });

    it("defines border radius variables", () => {
      expect(cssContent).toContain("--radius-sm");
      expect(cssContent).toContain("--radius:");
      expect(cssContent).toContain("--radius-md");
      expect(cssContent).toContain("--radius-lg");
    });

    it("defines shadow variables", () => {
      expect(cssContent).toContain("--shadow-sm");
      expect(cssContent).toContain("--shadow:");
      expect(cssContent).toContain("--shadow-md");
      expect(cssContent).toContain("--shadow-lg");
    });

    it("defines transition variables", () => {
      expect(cssContent).toContain("--transition-fast");
      expect(cssContent).toContain("--transition-base");
    });
  });

  describe("CSS Reset", () => {
    it("includes box-sizing reset", () => {
      expect(cssContent).toContain("box-sizing: border-box");
    });

    it("resets margin and padding on universal selector", () => {
      expect(cssContent).toContain("margin: 0");
      expect(cssContent).toContain("padding: 0");
    });

    it("sets body min-height to 100vh", () => {
      expect(cssContent).toContain("min-height: 100vh");
    });

    it("removes default list styles", () => {
      expect(cssContent).toContain("list-style: none");
    });
  });

  describe("Responsive container", () => {
    it("defines a max-width for the app container", () => {
      expect(cssContent).toContain("--container-max-width");
      expect(cssContent).toContain("max-width: var(--container-max-width)");
    });

    it("centers the container with margin auto", () => {
      expect(cssContent).toContain("margin: 0 auto");
    });

    it("includes responsive media queries", () => {
      expect(cssContent).toContain("@media");
      expect(cssContent).toContain("max-width: 480px");
    });
  });

  describe("Card aesthetic", () => {
    it("defines a card class with background and border", () => {
      expect(cssContent).toContain(".card");
      expect(cssContent).toContain("border: var(--border)");
      expect(cssContent).toContain("border-radius: var(--radius-md)");
    });

    it("applies shadow to card", () => {
      expect(cssContent).toContain("box-shadow: var(--shadow-sm)");
    });

    it("includes hover shadow transition on card", () => {
      expect(cssContent).toContain(".card:hover");
      expect(cssContent).toContain("box-shadow: var(--shadow)");
    });
  });

  describe("Layout selectors", () => {
    it("defines .app layout class", () => {
      expect(cssContent).toContain(".app {");
    });

    it("defines .app-header class", () => {
      expect(cssContent).toContain(".app-header");
    });

    it("defines .app-main class", () => {
      expect(cssContent).toContain(".app-main");
    });

    it("defines .app-footer class", () => {
      expect(cssContent).toContain(".app-footer");
    });
  });
});
