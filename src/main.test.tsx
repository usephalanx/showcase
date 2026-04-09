import { describe, it, expect, vi, beforeEach } from "vitest";

/**
 * Unit tests for the main entry point module.
 *
 * Verifies that createRoot is called with the correct DOM element
 * and that render is invoked.
 */
describe("main.tsx", () => {
  const mockRender = vi.fn();
  const mockCreateRoot = vi.fn(() => ({ render: mockRender }));

  beforeEach(() => {
    vi.resetModules();
    mockRender.mockClear();
    mockCreateRoot.mockClear();

    // Create a mock #root element in the DOM
    const rootDiv = document.createElement("div");
    rootDiv.id = "root";
    document.body.appendChild(rootDiv);

    // Mock react-dom/client
    vi.doMock("react-dom/client", () => ({
      createRoot: mockCreateRoot,
    }));
  });

  it("calls createRoot with the #root element and renders", async () => {
    await import("./main");

    const rootElement = document.getElementById("root");
    expect(mockCreateRoot).toHaveBeenCalledTimes(1);
    expect(mockCreateRoot).toHaveBeenCalledWith(rootElement);
    expect(mockRender).toHaveBeenCalledTimes(1);
  });
});
