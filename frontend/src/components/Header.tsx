import React, { useState, useEffect } from 'react';

export interface NavLink {
  label: string;
  href: string;
}

export interface HeaderProps {
  logoText: string;
  navLinks: NavLink[];
  ctaText: string;
  ctaHref: string;
}

const Header: React.FC<HeaderProps> = ({ logoText, navLinks, ctaText, ctaHref }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const toggleMobileMenu = () => {
    setMobileMenuOpen((prev) => !prev);
  };

  const handleLinkClick = () => {
    setMobileMenuOpen(false);
  };

  return (
    <header
      className={`sticky top-0 z-50 w-full backdrop-blur-md bg-white/80 transition-shadow duration-300 ${
        scrolled ? 'shadow-md' : 'shadow-none'
      }`}
      data-testid="header"
    >
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        {/* Logo */}
        <a
          href="#hero"
          className="font-playfair text-xl font-bold tracking-tight text-slate-800"
          data-testid="header-logo"
          onClick={handleLinkClick}
        >
          {logoText}
        </a>

        {/* Desktop Nav Links */}
        <ul className="hidden items-center gap-8 md:flex" data-testid="desktop-nav">
          {navLinks.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                className="font-inter text-sm font-medium text-slate-600 transition-colors duration-200 hover:text-gold-600"
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        {/* Desktop CTA */}
        <a
          href={ctaHref}
          className="hidden rounded-md bg-gold-500 px-5 py-2 font-inter text-sm font-semibold text-white shadow-sm transition-colors duration-200 hover:bg-gold-600 md:inline-block"
          data-testid="header-cta"
        >
          {ctaText}
        </a>

        {/* Mobile Hamburger Button */}
        <button
          type="button"
          className="inline-flex items-center justify-center rounded-md p-2 text-slate-700 hover:bg-slate-100 focus:outline-none focus:ring-2 focus:ring-gold-500 md:hidden"
          onClick={toggleMobileMenu}
          aria-expanded={mobileMenuOpen}
          aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
          data-testid="mobile-menu-button"
        >
          {mobileMenuOpen ? (
            <svg
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              aria-hidden="true"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            <svg
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              aria-hidden="true"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
            </svg>
          )}
        </button>
      </nav>

      {/* Mobile Slide-Down Menu */}
      <div
        className={`overflow-hidden transition-all duration-300 ease-in-out md:hidden ${
          mobileMenuOpen ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'
        }`}
        data-testid="mobile-menu"
      >
        <div className="border-t border-slate-200 bg-white/95 px-4 pb-4 pt-2">
          <ul className="flex flex-col gap-1">
            {navLinks.map((link) => (
              <li key={link.href}>
                <a
                  href={link.href}
                  className="block rounded-md px-3 py-2 font-inter text-base font-medium text-slate-700 transition-colors duration-200 hover:bg-cream-100 hover:text-gold-600"
                  onClick={handleLinkClick}
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
          <a
            href={ctaHref}
            className="mt-3 block w-full rounded-md bg-gold-500 px-5 py-2.5 text-center font-inter text-sm font-semibold text-white shadow-sm transition-colors duration-200 hover:bg-gold-600"
            onClick={handleLinkClick}
            data-testid="mobile-cta"
          >
            {ctaText}
          </a>
        </div>
      </div>
    </header>
  );
};

export default Header;
