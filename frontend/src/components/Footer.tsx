import React from 'react';

export interface FooterLogo {
  /** Text or element to render as the logo */
  text: string;
  /** Optional className for the logo */
  className?: string;
}

export interface SocialLink {
  /** Unique identifier */
  id: string;
  /** Platform name (used for aria-label) */
  platform: string;
  /** URL the icon links to */
  href: string;
  /** SVG path data or icon element */
  icon: React.ReactNode;
}

export interface FooterProps {
  /** Logo text displayed in sm variant */
  logoText: string;
  /** Tagline displayed below the logo */
  tagline?: string;
  /** Social media links */
  socialLinks?: SocialLink[];
  /** Copyright text */
  copyright?: string;
  /** Optional additional className for the footer */
  className?: string;
}

const Footer: React.FC<FooterProps> = ({
  logoText,
  tagline = 'Luxury real estate, personal touch.',
  socialLinks = [],
  copyright = '© 2025 Maddie Real Estate. All rights reserved.',
  className = '',
}) => {
  return (
    <footer
      className={`bg-slate-800 border-t border-[#C8A951] py-8 ${className}`.trim()}
      data-testid="footer"
    >
      <div className="max-w-7xl mx-auto px-4 flex flex-col items-center text-center gap-4">
        {/* Logo - sm variant */}
        <div
          className="font-['Playfair_Display'] text-xl font-semibold text-white tracking-wide"
          data-testid="footer-logo"
        >
          {logoText}
        </div>

        {/* Tagline */}
        {tagline && (
          <p
            className="font-['Inter'] italic text-sm text-slate-300"
            data-testid="footer-tagline"
          >
            {tagline}
          </p>
        )}

        {/* Social Icons */}
        {socialLinks.length > 0 && (
          <div
            className="flex items-center gap-4 mt-2"
            data-testid="footer-social-icons"
          >
            {socialLinks.map((link) => (
              <a
                key={link.id}
                href={link.href}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={link.platform}
                className="text-slate-400 hover:text-[#D4B968] transition-colors duration-200"
              >
                {link.icon}
              </a>
            ))}
          </div>
        )}

        {/* Copyright */}
        {copyright && (
          <p
            className="font-['Inter'] text-xs text-slate-400 mt-2"
            data-testid="footer-copyright"
          >
            {copyright}
          </p>
        )}
      </div>
    </footer>
  );
};

export default Footer;
