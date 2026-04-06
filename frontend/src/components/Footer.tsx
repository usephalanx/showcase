import React from 'react';

export interface FooterLink {
  label: string;
  href: string;
}

export interface SocialLink {
  platform: string;
  href: string;
  iconPath: string;
}

export interface ContactInfo {
  address: string;
  phone: string;
  email: string;
}

export interface FooterProps {
  brandName: string;
  brandDescription: string;
  quickLinks: FooterLink[];
  contactInfo: ContactInfo;
  socialLinks: SocialLink[];
  copyrightYear: number;
  onNavigate?: (href: string) => void;
}

const Footer: React.FC<FooterProps> = ({
  brandName,
  brandDescription,
  quickLinks,
  contactInfo,
  socialLinks,
  copyrightYear,
  onNavigate,
}) => {
  const handleClick = (href: string) => {
    onNavigate?.(href);
  };

  return (
    <footer data-testid="footer" className="bg-gray-900 text-gray-300">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8 lg:py-16">
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {/* Brand column */}
          <div data-testid="footer-brand">
            <h3 className="text-lg font-bold text-white">{brandName}</h3>
            <p className="mt-3 text-sm leading-relaxed text-gray-400">
              {brandDescription}
            </p>
          </div>

          {/* Quick Links column */}
          <div data-testid="footer-quick-links">
            <h4 className="text-sm font-semibold uppercase tracking-wider text-white">
              Quick Links
            </h4>
            <ul className="mt-4 space-y-2">
              {quickLinks.map((link) => (
                <li key={link.href}>
                  <button
                    onClick={() => handleClick(link.href)}
                    className="text-sm text-gray-400 transition-colors hover:text-white"
                  >
                    {link.label}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact column */}
          <div data-testid="footer-contact">
            <h4 className="text-sm font-semibold uppercase tracking-wider text-white">
              Contact Us
            </h4>
            <ul className="mt-4 space-y-2 text-sm text-gray-400">
              <li className="flex items-start gap-2">
                <svg className="mt-0.5 h-4 w-4 flex-shrink-0 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span>{contactInfo.address}</span>
              </li>
              <li className="flex items-center gap-2">
                <svg className="h-4 w-4 flex-shrink-0 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                <span>{contactInfo.phone}</span>
              </li>
              <li className="flex items-center gap-2">
                <svg className="h-4 w-4 flex-shrink-0 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <span>{contactInfo.email}</span>
              </li>
            </ul>
          </div>

          {/* Social column */}
          <div data-testid="footer-social">
            <h4 className="text-sm font-semibold uppercase tracking-wider text-white">
              Follow Us
            </h4>
            <div className="mt-4 flex gap-3">
              {socialLinks.map((social) => (
                <a
                  key={social.platform}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={social.platform}
                  className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-800 text-gray-400 transition-colors hover:bg-gray-700 hover:text-white"
                >
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d={social.iconPath} />
                  </svg>
                </a>
              ))}
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div
          className="mt-12 border-t border-gray-800 pt-8 text-center text-sm text-gray-500"
          data-testid="footer-copyright"
        >
          &copy; {copyrightYear} {brandName}. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
