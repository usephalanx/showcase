import React from "react";
import { NavLink } from "react-router-dom";

/**
 * Navigation link descriptor used by the Header component.
 */
export interface NavItem {
  /** Display label for the link. */
  label: string;
  /** Route path for React Router NavLink. */
  to: string;
}

/**
 * Props for the Header component.
 */
export interface HeaderProps {
  /** Site title displayed next to the logo area. */
  siteTitle: string;
  /** Navigation links rendered in the header. */
  navItems: NavItem[];
  /** Placeholder text for the search input. */
  searchPlaceholder?: string;
  /** Callback fired when the search input value changes. */
  onSearchChange?: (value: string) => void;
  /** Current value of the search input (controlled). */
  searchValue?: string;
  /** Optional URL or path for the logo/title link. Defaults to "/". */
  logoLinkTo?: string;
}

const styles: Record<string, React.CSSProperties> = {
  header: {
    position: "sticky",
    top: 0,
    zIndex: 1000,
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 24px",
    height: 56,
    backgroundColor: "#ffffff",
    boxShadow: "0 1px 3px rgba(0, 0, 0, 0.1)",
    fontFamily: "'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif",
  },
  logoLink: {
    textDecoration: "none",
    color: "#111827",
    display: "flex",
    alignItems: "center",
    gap: 8,
    flexShrink: 0,
  },
  logoIcon: {
    width: 28,
    height: 28,
    borderRadius: 6,
    backgroundColor: "#4f46e5",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "#ffffff",
    fontSize: 14,
    fontWeight: 700,
  },
  siteTitle: {
    fontSize: 18,
    fontWeight: 700,
    letterSpacing: "-0.01em",
    color: "#111827",
    margin: 0,
  },
  nav: {
    display: "flex",
    alignItems: "center",
    gap: 4,
    margin: "0 24px",
  },
  navLinkBase: {
    textDecoration: "none",
    fontSize: 14,
    fontWeight: 500,
    padding: "6px 12px",
    borderRadius: 6,
    color: "#6b7280",
    transition: "color 0.15s, background-color 0.15s",
  },
  navLinkActive: {
    color: "#4f46e5",
    backgroundColor: "#eef2ff",
  },
  searchWrapper: {
    position: "relative" as const,
    flexShrink: 0,
  },
  searchInput: {
    fontSize: 14,
    padding: "6px 12px 6px 32px",
    border: "1px solid #e5e7eb",
    borderRadius: 8,
    outline: "none",
    width: 200,
    backgroundColor: "#f9fafb",
    color: "#111827",
    transition: "border-color 0.15s, box-shadow 0.15s",
  },
  searchIcon: {
    position: "absolute" as const,
    left: 10,
    top: "50%",
    transform: "translateY(-50%)",
    width: 14,
    height: 14,
    color: "#9ca3af",
    pointerEvents: "none" as const,
  },
};

/**
 * Header navigation bar with site branding, nav links, and search input.
 *
 * Uses React Router `NavLink` for navigation with automatic active styling.
 * The header is sticky-positioned with a subtle bottom shadow.
 */
const Header: React.FC<HeaderProps> = ({
  siteTitle,
  navItems,
  searchPlaceholder = "Search…",
  onSearchChange,
  searchValue = "",
  logoLinkTo = "/",
}) => {
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onSearchChange?.(e.target.value);
  };

  return (
    <header style={styles.header} data-testid="header">
      <NavLink to={logoLinkTo} style={styles.logoLink} aria-label={siteTitle}>
        <span style={styles.logoIcon} aria-hidden="true">
          K
        </span>
        <span style={styles.siteTitle}>{siteTitle}</span>
      </NavLink>

      <nav style={styles.nav} data-testid="header-nav" aria-label="Main navigation">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            style={({ isActive }) => ({
              ...styles.navLinkBase,
              ...(isActive ? styles.navLinkActive : {}),
            })}
            data-testid={`nav-link-${item.label.toLowerCase()}`}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div style={styles.searchWrapper}>
        <svg
          style={styles.searchIcon}
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
          aria-hidden="true"
        >
          <path
            fillRule="evenodd"
            d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z"
            clipRule="evenodd"
          />
        </svg>
        <input
          type="search"
          placeholder={searchPlaceholder}
          value={searchValue}
          onChange={handleSearchChange}
          style={styles.searchInput}
          data-testid="header-search"
          aria-label={searchPlaceholder}
        />
      </div>
    </header>
  );
};

export default Header;
