import React, { useState, useEffect, useCallback } from 'react';

export interface NavLink {
  label: string;
  href: string;
}

export interface HeaderProps {
  brandName: string;
  navLinks: NavLink[];
  onNavigate?: (href: string) => void;
}

const Header: React.FC<HeaderProps> = ({ brandName, navLinks, onNavigate }) => {
  const [scrolled, setScrolled] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    if (drawerOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [drawerOpen]);

  const handleLinkClick = useCallback(
    (href: string) => {
      setDrawerOpen(false);
      onNavigate?.(href);
    },
    [onNavigate]
  );

  return (
    <>
      <header
        data-testid="header"
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          scrolled
            ? 'bg-white shadow-lg backdrop-blur-sm'
            : 'bg-transparent'
        }`}
      >
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between sm:h-20">
            {/* Brand */}
            <button
              onClick={() => handleLinkClick('/')}
              className={`text-xl font-bold tracking-tight transition-colors duration-300 sm:text-2xl ${
                scrolled ? 'text-gray-900' : 'text-white'
              }`}
              data-testid="brand-name"
            >
              {brandName}
            </button>

            {/* Desktop nav */}
            <nav className="hidden md:flex md:items-center md:gap-8" data-testid="desktop-nav">
              {navLinks.map((link) => (
                <button
                  key={link.href}
                  onClick={() => handleLinkClick(link.href)}
                  className={`text-sm font-medium transition-colors duration-300 hover:opacity-80 ${
                    scrolled ? 'text-gray-700 hover:text-gray-900' : 'text-white/90 hover:text-white'
                  }`}
                >
                  {link.label}
                </button>
              ))}
            </nav>

            {/* Mobile hamburger */}
            <button
              onClick={() => setDrawerOpen(true)}
              className="flex md:hidden flex-col items-center justify-center gap-1.5 p-2"
              aria-label="Open menu"
              data-testid="hamburger-button"
            >
              <span
                className={`block h-0.5 w-6 transition-colors duration-300 ${
                  scrolled ? 'bg-gray-900' : 'bg-white'
                }`}
              />
              <span
                className={`block h-0.5 w-6 transition-colors duration-300 ${
                  scrolled ? 'bg-gray-900' : 'bg-white'
                }`}
              />
              <span
                className={`block h-0.5 w-6 transition-colors duration-300 ${
                  scrolled ? 'bg-gray-900' : 'bg-white'
                }`}
              />
            </button>
          </div>
        </div>
      </header>

      {/* Mobile drawer overlay */}
      {drawerOpen && (
        <div
          className="fixed inset-0 z-50 bg-black/50 transition-opacity duration-300"
          onClick={() => setDrawerOpen(false)}
          data-testid="drawer-overlay"
        />
      )}

      {/* Mobile drawer */}
      <div
        data-testid="mobile-drawer"
        className={`fixed top-0 right-0 z-50 h-full w-72 transform bg-white shadow-2xl transition-transform duration-300 ease-in-out ${
          drawerOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between border-b border-gray-100 px-6 py-5">
          <span className="text-lg font-bold text-gray-900">{brandName}</span>
          <button
            onClick={() => setDrawerOpen(false)}
            aria-label="Close menu"
            data-testid="close-drawer-button"
            className="rounded-md p-1 text-gray-500 hover:bg-gray-100 hover:text-gray-900"
          >
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <nav className="flex flex-col px-6 py-4">
          {navLinks.map((link) => (
            <button
              key={link.href}
              onClick={() => handleLinkClick(link.href)}
              className="border-b border-gray-50 py-3 text-left text-base font-medium text-gray-700 transition-colors hover:text-gray-900"
            >
              {link.label}
            </button>
          ))}
        </nav>
      </div>
    </>
  );
};

export default Header;
