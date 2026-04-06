import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import Layout, { LayoutProps } from "./Layout";
import { NavLink } from "./Navbar";

const defaultNavLinks: NavLink[] = [
  { label: "Boards", href: "/boards", isActive: false },
  { label: "Tags", href: "/tags", isActive: false },
];

function renderLayout(overrides: Partial<LayoutProps> = {}) {
  const props: LayoutProps = {
    siteTitle: "KanbanFlow",
    navLinks: defaultNavLinks,
    children: <div data-testid="page-content">Page Content</div>,
    ...overrides,
  };
  return render(<Layout {...props} />);
}

describe("Layout", () => {
  it("renders without crashing", () => {
    renderLayout();
    expect(screen.getByRole("navigation")).toBeInTheDocument();
    expect(screen.getByRole("main")).toBeInTheDocument();
    expect(screen.getByRole("contentinfo")).toBeInTheDocument();
  });

  it("renders the Navbar with site title", () => {
    renderLayout({ siteTitle: "TestBoard" });
    expect(screen.getByText("TestBoard")).toBeInTheDocument();
  });

  it("renders children in the main content area", () => {
    renderLayout();
    const main = screen.getByRole("main");
    expect(main).toContainElement(screen.getByTestId("page-content"));
    expect(screen.getByText("Page Content")).toBeInTheDocument();
  });

  it("renders default footer text with site title and year", () => {
    renderLayout({ siteTitle: "KanbanFlow" });
    const year = new Date().getFullYear();
    expect(
      screen.getByText(`© ${year} KanbanFlow. All rights reserved.`)
    ).toBeInTheDocument();
  });

  it("renders custom footer text when provided", () => {
    renderLayout({ footerText: "Custom Footer" });
    expect(screen.getByText("Custom Footer")).toBeInTheDocument();
  });

  it("renders footer children when provided", () => {
    renderLayout({
      footerChildren: <a href="/privacy">Privacy Policy</a>,
    });
    expect(screen.getByText("Privacy Policy")).toBeInTheDocument();
  });

  it("does not render footer children container when not provided", () => {
    const { container } = renderLayout({ footerChildren: undefined });
    const footer = container.querySelector("footer");
    // Only one child div inside footer (the text paragraph)
    const innerDivs = footer!.querySelector(".flex")!.children;
    expect(innerDivs.length).toBe(1);
  });

  it("passes onNavLinkClick to Navbar", () => {
    const onNavLinkClick = vi.fn();
    renderLayout({ onNavLinkClick });
    const boardsLink = screen.getAllByText("Boards")[0];
    fireEvent.click(boardsLink);
    expect(onNavLinkClick).toHaveBeenCalledWith("/boards");
  });

  it("renders navigation links", () => {
    renderLayout();
    expect(screen.getAllByText("Boards").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Tags").length).toBeGreaterThanOrEqual(1);
  });

  it("renders with complex children", () => {
    renderLayout({
      children: (
        <div>
          <h1>Board Title</h1>
          <p>Board description here</p>
          <ul>
            <li>Column 1</li>
            <li>Column 2</li>
          </ul>
        </div>
      ),
    });
    expect(screen.getByText("Board Title")).toBeInTheDocument();
    expect(screen.getByText("Column 1")).toBeInTheDocument();
    expect(screen.getByText("Column 2")).toBeInTheDocument();
  });

  it("passes siteTitleHref to Navbar", () => {
    const onNavLinkClick = vi.fn();
    renderLayout({ siteTitleHref: "/dashboard", onNavLinkClick });
    fireEvent.click(screen.getByText("KanbanFlow"));
    expect(onNavLinkClick).toHaveBeenCalledWith("/dashboard");
  });
});
