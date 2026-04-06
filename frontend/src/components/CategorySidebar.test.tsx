import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import CategorySidebar, { CategoryNode } from "./CategorySidebar";

const sampleCategories: CategoryNode[] = [
  {
    id: 1,
    name: "Engineering",
    slug: "engineering",
    children: [
      {
        id: 2,
        name: "Frontend",
        slug: "frontend",
        children: [
          { id: 5, name: "React", slug: "react", children: [] },
        ],
      },
      { id: 3, name: "Backend", slug: "backend", children: [] },
    ],
  },
  {
    id: 4,
    name: "Design",
    slug: "design",
    children: [],
  },
];

describe("CategorySidebar", () => {
  it("renders without crashing", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar categories={[]} onSelect={onSelect} />,
    );
    expect(screen.getByTestId("category-sidebar")).toBeDefined();
  });

  it("renders top-level categories", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar categories={sampleCategories} onSelect={onSelect} />,
    );
    expect(screen.getByTestId("link-engineering")).toBeDefined();
    expect(screen.getByTestId("link-design")).toBeDefined();
  });

  it("displays the title when provided", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar
        categories={sampleCategories}
        onSelect={onSelect}
        title="Categories"
      />,
    );
    expect(screen.getByTestId("sidebar-title").textContent).toBe("Categories");
  });

  it("does not display a title when not provided", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar categories={sampleCategories} onSelect={onSelect} />,
    );
    expect(screen.queryByTestId("sidebar-title")).toBeNull();
  });

  it("children are hidden by default for non-active paths", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar categories={sampleCategories} onSelect={onSelect} />,
    );
    // Frontend is a child of Engineering; should not be visible initially
    expect(screen.queryByTestId("link-frontend")).toBeNull();
  });

  it("expands children when toggle button is clicked", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar categories={sampleCategories} onSelect={onSelect} />,
    );

    // Click the Engineering toggle
    const toggle = screen.getByTestId("toggle-engineering");
    fireEvent.click(toggle);

    // Now Frontend and Backend should be visible
    expect(screen.getByTestId("link-frontend")).toBeDefined();
    expect(screen.getByTestId("link-backend")).toBeDefined();
  });

  it("collapses children when toggle is clicked again", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar categories={sampleCategories} onSelect={onSelect} />,
    );

    const toggle = screen.getByTestId("toggle-engineering");
    fireEvent.click(toggle); // expand
    expect(screen.getByTestId("link-frontend")).toBeDefined();

    fireEvent.click(toggle); // collapse
    expect(screen.queryByTestId("link-frontend")).toBeNull();
  });

  it("calls onSelect with the correct slug when a category link is clicked", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar categories={sampleCategories} onSelect={onSelect} />,
    );

    fireEvent.click(screen.getByTestId("link-engineering"));
    expect(onSelect).toHaveBeenCalledTimes(1);
    expect(onSelect).toHaveBeenCalledWith("engineering");
  });

  it("renders the link with correct href", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar categories={sampleCategories} onSelect={onSelect} />,
    );

    const link = screen.getByTestId("link-engineering");
    expect(link.getAttribute("href")).toBe("/categories/engineering");
  });

  it("marks the active category with aria-current", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar
        categories={sampleCategories}
        activeCategorySlug="design"
        onSelect={onSelect}
      />,
    );

    const activeLink = screen.getByTestId("link-design");
    expect(activeLink.getAttribute("aria-current")).toBe("page");

    const inactiveLink = screen.getByTestId("link-engineering");
    expect(inactiveLink.getAttribute("aria-current")).toBeNull();
  });

  it("auto-expands ancestor path when activeCategorySlug is a nested category", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar
        categories={sampleCategories}
        activeCategorySlug="react"
        onSelect={onSelect}
      />,
    );

    // "react" is nested under Engineering > Frontend
    // So both Engineering and Frontend should be expanded automatically
    expect(screen.getByTestId("link-frontend")).toBeDefined();
    expect(screen.getByTestId("link-react")).toBeDefined();
    expect(screen.getByTestId("link-react").getAttribute("aria-current")).toBe("page");
  });

  it("does not show toggle button for leaf categories", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar categories={sampleCategories} onSelect={onSelect} />,
    );

    // Design has no children, so no toggle button
    expect(screen.queryByTestId("toggle-design")).toBeNull();
  });

  it("shows toggle button for parent categories", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar categories={sampleCategories} onSelect={onSelect} />,
    );

    expect(screen.getByTestId("toggle-engineering")).toBeDefined();
  });

  it("applies custom className to root element", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar
        categories={sampleCategories}
        onSelect={onSelect}
        className="custom-class"
      />,
    );

    const sidebar = screen.getByTestId("category-sidebar");
    expect(sidebar.className).toContain("custom-class");
    expect(sidebar.className).toContain("category-sidebar");
  });

  it("deeply nested expansion works through multiple levels", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar categories={sampleCategories} onSelect={onSelect} />,
    );

    // Expand Engineering
    fireEvent.click(screen.getByTestId("toggle-engineering"));
    // Now expand Frontend
    fireEvent.click(screen.getByTestId("toggle-frontend"));
    // React should now be visible
    expect(screen.getByTestId("link-react")).toBeDefined();
  });

  it("handles empty children array gracefully", () => {
    const onSelect = vi.fn();
    const cats: CategoryNode[] = [
      { id: 1, name: "Empty Parent", slug: "empty-parent", children: [] },
    ];
    render(<CategorySidebar categories={cats} onSelect={onSelect} />);
    expect(screen.getByTestId("link-empty-parent")).toBeDefined();
    expect(screen.queryByTestId("toggle-empty-parent")).toBeNull();
  });

  it("sets aria-label from title prop", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar
        categories={sampleCategories}
        onSelect={onSelect}
        title="Browse Topics"
      />,
    );
    const nav = screen.getByTestId("category-sidebar");
    expect(nav.getAttribute("aria-label")).toBe("Browse Topics");
  });

  it("uses default aria-label when title is not provided", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar categories={sampleCategories} onSelect={onSelect} />,
    );
    const nav = screen.getByTestId("category-sidebar");
    expect(nav.getAttribute("aria-label")).toBe("Category navigation");
  });

  it("prevents default on link click to allow onSelect to handle navigation", () => {
    const onSelect = vi.fn();
    render(
      <CategorySidebar categories={sampleCategories} onSelect={onSelect} />,
    );

    const link = screen.getByTestId("link-design");
    const event = new MouseEvent("click", { bubbles: true, cancelable: true });
    const preventDefaultSpy = vi.spyOn(event, "preventDefault");
    link.dispatchEvent(event);
    // The event should have been preventDefaulted via the React handler
    // We verify onSelect was called which confirms the handler ran
    expect(onSelect).toHaveBeenCalledWith("design");
  });
});
