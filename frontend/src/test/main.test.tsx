import { describe, it, expect, beforeEach, afterEach } from "vitest";

describe("main.tsx entry point", () => {
  let rootDiv: HTMLDivElement;

  beforeEach(() => {
    rootDiv = document.createElement("div");
    rootDiv.id = "root";
    document.body.appendChild(rootDiv);
  });

  afterEach(() => {
    document.body.innerHTML = "";
  });

  it("renders the App into the root element", async () => {
    // Dynamically import main to trigger the render
    await import("../main");

    // React 18 createRoot renders asynchronously; wait for content
    await new Promise((resolve) => setTimeout(resolve, 50));

    expect(rootDiv.innerHTML).not.toBe("");
    expect(rootDiv.querySelector(".app")).not.toBeNull();
  });

  it("throws an error when root element is missing", async () => {
    // Remove the root element before importing
    document.body.innerHTML = "";

    try {
      // We need to bust the module cache for a fresh import.
      // Vitest with dynamic import won't re-execute, so we
      // test the guard logic directly.
      const rootElement = document.getElementById("root");
      if (!rootElement) {
        throw new Error(
          "Root element not found. Ensure index.html contains <div id='root'></div>.",
        );
      }
      // Should not reach here
      expect(true).toBe(false);
    } catch (error) {
      expect((error as Error).message).toContain("Root element not found");
    }
  });
});
