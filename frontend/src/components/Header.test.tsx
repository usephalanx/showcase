import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Header, { HeaderProps, NavItem } from "./Header";

const defaultNavItems: NavItem[] = [
  { label: "Home", to: "/" },
  { label: "Boards", to: "/boards" },
  { label: "Categories", to: "/categories" },
];

const defaultProps: HeaderProps = {
  siteTitle: "Kanban App",
  navItems: defaultNavItems,
};

function renderHeader(props: Partial<HeaderProps> = {}) {
  return render(
    <MemoryRouter initialEntries={["/"]}>
      <Header {...defaultProps} {...props} />
    </MemoryRouter>,
  );
}

describe("Header", () => {
  it("renders without crashing", () => {
    renderHeader();
    expect(screen.getByTestId("header")).toBeDefined();
  });

  it("displays the site title", () => {
    renderHeader({ siteTitle: "My Board" });
    expect(screen.getByText("My Board")).toBeDefined();
  });

  it("renders all navigation links", () => {
    renderHeader();
    expect(screen.getByTestId("nav-link-home")).toBeDefined();
    expect(screen.getByTestId("nav-link-boards")).toBeDefined();
    expect(screen.getByTestId("nav-link-categories")).toBeDefined();
  });

  it("navigation links have correct text", () => {
    renderHeader();
    expect(screen.getByText("Home")).toBeDefined();
    expect(screen.getByText("Boards")).toBeDefined();
    expect(screen.getByText("Categories")).toBeDefined();
  });

  it("navigation links point to correct routes", () => {
    renderHeader();
    const homeLink = screen.getByTestId("nav-link-home");
    const boardsLink = screen.getByTestId("nav-link-boards");
    const categoriesLink = screen.getByTestId("nav-link-categories");

    expect(homeLink.getAttribute("href")).toBe("/");
    expect(boardsLink.getAttribute("href")).toBe("/boards");
    expect(categoriesLink.getAttribute("href")).toBe("/categories");
  });

  it("renders the search input with default placeholder", () => {
    renderHeader();
    const searchInput = screen.getByTestId("header-search") as HTMLInputElement;
    expect(searchInput).toBeDefined();
    expect(searchInput.placeholder).toBe("Search…");
  });

  it("renders the search input with a custom placeholder", () => {
    renderHeader({ searchPlaceholder: "Find boards..." });
    const searchInput = screen.getByTestId("header-search") as HTMLInputElement;
    expect(searchInput.placeholder).toBe("Find boards...");
  });

  it("calls onSearchChange when typing in the search input", () => {
    const onSearchChange = vi.fn();
    renderHeader({ onSearchChange, searchValue: "" });
    const searchInput = screen.getByTestId("header-search");

    fireEvent.change(searchInput, { target: { value: "test query" } });
    expect(onSearchChange).toHaveBeenCalledTimes(1);
    expect(onSearchChange).toHaveBeenCalledWith("test query");
  });

  it("displays the controlled search value", () => {
    renderHeader({ searchValue: "hello" });
    const searchInput = screen.getByTestId("header-search") as HTMLInputElement;
    expect(searchInput.value).toBe("hello");
  });

  it("renders with empty nav items", () => {
    renderHeader({ navItems: [] });
    const nav = screen.getByTestId("header-nav");
    expect(nav.children.length).toBe(0);
  });

  it("renders with custom nav items", () => {
    const customItems: NavItem[] = [
      { label: "Dashboard", to: "/dashboard" },
      { label: "Settings", to: "/settings" },
    ];
    renderHeader({ navItems: customItems });
    expect(screen.getByText("Dashboard")).toBeDefined();
    expect(screen.getByText("Settings")).toBeDefined();
  });

  it("has a sticky header element", () => {
    renderHeader();
    const header = screen.getByTestId("header");
    expect(header.style.position).toBe("sticky");
    expect(header.style.top).toBe("0px");
  });

  it("has the logo link pointing to logoLinkTo", () => {
    renderHeader({ logoLinkTo: "/home" });
    const logoLink = screen.getByLabelText("Kanban App");
    expect(logoLink.getAttribute("href")).toBe("/home");
  });

  it("logo link defaults to /", () => {
    renderHeader();
    const logoLink = screen.getByLabelText("Kanban App");
    expect(logoLink.getAttribute("href")).toBe("/");
  });

  it("has proper aria-label on nav element", () => {
    renderHeader();
    const nav = screen.getByRole("navigation", { name: "Main navigation" });
    expect(nav).toBeDefined();
  });

  it("does not call onSearchChange when not provided", () => {
    // Should not throw when onSearchChange is undefined
    renderHeader({ onSearchChange: undefined });
    const searchInput = screen.getByTestId("header-search");
    expect(() => {
      fireEvent.change(searchInput, { target: { value: "x" } });
    }).not.toThrow();
  });
});
