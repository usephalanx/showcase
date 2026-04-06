import { useState, useCallback, useEffect, useRef } from "react";

export interface NavLink {
  /** Display label for the navigation link */
  label: string;
  /** URL or route path */
  href: string;
  /** Whether this link is currently active */
  isActive?: boolean;
}

export interface NavbarProps {
  /** Site title or brand name displayed in the navbar */
  siteTitle: string;
  /** URL the site title links to */
  siteTitleHref?: string;
  /** Navigation links to render */
  links: NavLink[];
  /** Callback when a navigation link is clicked */
  onLinkClick?: (href: string) => void;
  /** Optional aria-label for the nav element */
  ariaLabel?: string;
}

export default function Navbar({
  siteTitle,
  siteTitleHref = "/",
  links,
  onLinkClick,
  ariaLabel = "Main navigation",
}: NavbarProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const toggleMobileMenu = useCallback(() => {
    setIsMobileMenuOpen((prev) => !prev);
  }, []);

  const handleLinkClick = useCallback(
    (href: string) => {
      setIsMobileMenuOpen(false);
      onLinkClick?.(href);
    },
    [onLinkClick]
  );

  // Close mobile menu on Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isMobileMenuOpen) {
        setIsMobileMenuOpen(false);
        buttonRef.current?.focus();
      }
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isMobileMenuOpen]);

  // Close mobile menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        isMobileMenuOpen &&
        menuRef.current &&
        !menuRef.current.contains(e.target as Node) &&
        buttonRef.current &&
        !buttonRef.current.contains(e.target as Node)
      ) {
        setIsMobileMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [isMobileMenuOpen]);

  const linkBaseStyle =
    "px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200";
  const linkActiveStyle = "bg-indigo-700 text-white";
  const linkInactiveStyle =
    "text-indigo-100 hover:bg-indigo-500 hover:text-white";
  const mobileLinkBaseStyle =
    "block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200";

  return (
    <nav
      aria-label={ariaLabel}
      className="sticky top-0 z-50 bg-indigo-600 shadow-lg"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex-shrink-0">
            <a
              href={siteTitleHref}
              onClick={(e) => {
                e.preventDefault();
                handleLinkClick(siteTitleHref);
              }}
              className="text-white text-xl font-bold tracking-tight hover:opacity-90 transition-opacity"
            >
              {siteTitle}
            </a>
          </div>

          {/* Desktop links */}
          <div className="hidden md:flex md:items-center md:space-x-1">
            {links.map((link) => (
              <a
                key={link.href}
                href={link.href}
                onClick={(e) => {
                  e.preventDefault();
                  handleLinkClick(link.href);
                }}
                className={`${linkBaseStyle} ${link.isActive ? linkActiveStyle : linkInactiveStyle}`}
                aria-current={link.isActive ? "page" : undefined}
              >
                {link.label}
              </a>
            ))}
          </div>

          {/* Mobile hamburger button */}
          <div className="md:hidden">
            <button
              ref={buttonRef}
              type="button"
              onClick={toggleMobileMenu}
              aria-expanded={isMobileMenuOpen}
              aria-controls="mobile-menu"
              aria-label={isMobileMenuOpen ? "Close menu" : "Open menu"}
              className="inline-flex items-center justify-center p-2 rounded-md text-indigo-100 hover:text-white hover:bg-indigo-500 transition-colors"
            >
              {isMobileMenuOpen ? (
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isMobileMenuOpen && (
        <div ref={menuRef} id="mobile-menu" className="md:hidden border-t border-indigo-500">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {links.map((link) => (
              <a
                key={link.href}
                href={link.href}
                onClick={(e) => {
                  e.preventDefault();
                  handleLinkClick(link.href);
                }}
                className={`${mobileLinkBaseStyle} ${link.isActive ? linkActiveStyle : linkInactiveStyle}`}
                aria-current={link.isActive ? "page" : undefined}
              >
                {link.label}
              </a>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
}
