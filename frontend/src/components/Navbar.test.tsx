import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import Navbar, { NavbarProps, NavLink } from "./Navbar";

const defaultLinks: NavLink[] = [
  { label: "Boards", href: "/boards", isActive: true },
  { label: "Tags", href: "/tags", isActive: false },
];

function renderNavbar(overrides: Partial<NavbarProps> = {}) {
  const props: NavbarProps = {
    siteTitle: "KanbanFlow",
    links: defaultLinks,
    ...overrides,
  };
  return render(<Navbar {...props} />);
}

describe("Navbar", () => {
  it("renders without crashing", () => {
    renderNavbar();
    expect(screen.getByRole("navigation")).toBeInTheDocument();
  });

  it("displays the site title", () => {
    renderNavbar({ siteTitle: "My Kanban" });
    expect(screen.getByText("My Kanban")).toBeInTheDocument();
  });

  it("renders all navigation links on desktop", () => {
    renderNavbar();
    const boardLinks = screen.getAllByText("Boards");
    expect(boardLinks.length).toBeGreaterThanOrEqual(1);
    const tagLinks = screen.getAllByText("Tags");
    expect(tagLinks.length).toBeGreaterThanOrEqual(1);
  });

  it("marks active link with aria-current='page'", () => {
    renderNavbar();
    const activeLinks = screen.getAllByText("Boards");
    const desktopActiveLink = activeLinks.find(
      (el) => el.getAttribute("aria-current") === "page"
    );
    expect(desktopActiveLink).toBeTruthy();
  });

  it("does not set aria-current on inactive links", () => {
    renderNavbar();
    const tagLinks = screen.getAllByText("Tags");
    tagLinks.forEach((el) => {
      expect(el.getAttribute("aria-current")).toBeNull();
    });
  });

  it("calls onLinkClick when a nav link is clicked", () => {
    const onLinkClick = vi.fn();
    renderNavbar({ onLinkClick });
    const boardsLink = screen.getAllByText("Boards")[0];
    fireEvent.click(boardsLink);
    expect(onLinkClick).toHaveBeenCalledWith("/boards");
  });

  it("calls onLinkClick with siteTitleHref when title is clicked", () => {
    const onLinkClick = vi.fn();
    renderNavbar({ onLinkClick, siteTitleHref: "/home" });
    fireEvent.click(screen.getByText("KanbanFlow"));
    expect(onLinkClick).toHaveBeenCalledWith("/home");
  });

  it("defaults siteTitleHref to '/' when not provided", () => {
    const onLinkClick = vi.fn();
    renderNavbar({ onLinkClick });
    fireEvent.click(screen.getByText("KanbanFlow"));
    expect(onLinkClick).toHaveBeenCalledWith("/");
  });

  it("toggles mobile menu open and closed", () => {
    renderNavbar();
    const menuButton = screen.getByLabelText("Open menu");
    expect(screen.queryByRole("link", { name: "Boards" })).toBeTruthy();

    // Open menu
    fireEvent.click(menuButton);
    expect(screen.getByLabelText("Close menu")).toBeInTheDocument();
    const mobileMenu = screen.getByRole("navigation").querySelector("#mobile-menu");
    expect(mobileMenu).toBeInTheDocument();

    // Close menu
    fireEvent.click(screen.getByLabelText("Close menu"));
    const mobileMenuAfter = screen.getByRole("navigation").querySelector("#mobile-menu");
    expect(mobileMenuAfter).toBeNull();
  });

  it("closes mobile menu when a link is clicked", () => {
    renderNavbar();
    const menuButton = screen.getByLabelText("Open menu");
    fireEvent.click(menuButton);

    const mobileMenu = screen.getByRole("navigation").querySelector("#mobile-menu");
    expect(mobileMenu).toBeInTheDocument();

    // Click a link inside mobile menu
    const mobileLinks = mobileMenu!.querySelectorAll("a");
    fireEvent.click(mobileLinks[0]);

    const mobileMenuAfter = screen.getByRole("navigation").querySelector("#mobile-menu");
    expect(mobileMenuAfter).toBeNull();
  });

  it("uses custom ariaLabel", () => {
    renderNavbar({ ariaLabel: "Site navigation" });
    expect(screen.getByLabelText("Site navigation")).toBeInTheDocument();
  });

  it("renders with empty links array", () => {
    renderNavbar({ links: [] });
    expect(screen.getByRole("navigation")).toBeInTheDocument();
    expect(screen.getByText("KanbanFlow")).toBeInTheDocument();
  });

  it("closes mobile menu on Escape key", () => {
    renderNavbar();
    const menuButton = screen.getByLabelText("Open menu");
    fireEvent.click(menuButton);
    expect(screen.getByRole("navigation").querySelector("#mobile-menu")).toBeInTheDocument();

    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.getByRole("navigation").querySelector("#mobile-menu")).toBeNull();
  });
});
