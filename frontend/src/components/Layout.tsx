import { ReactNode } from "react";
import Navbar, { NavLink } from "./Navbar";

export interface LayoutProps {
  /** Site title displayed in the navbar */
  siteTitle: string;
  /** URL the site title links to */
  siteTitleHref?: string;
  /** Navigation links for the navbar */
  navLinks: NavLink[];
  /** Callback when a navigation link is clicked */
  onNavLinkClick?: (href: string) => void;
  /** Main page content */
  children: ReactNode;
  /** Footer text content */
  footerText?: string;
  /** Optional extra footer content (e.g., links) */
  footerChildren?: ReactNode;
}

export default function Layout({
  siteTitle,
  siteTitleHref = "/",
  navLinks,
  onNavLinkClick,
  children,
  footerText,
  footerChildren,
}: LayoutProps) {
  const currentYear = new Date().getFullYear();
  const defaultFooterText = `© ${currentYear} ${siteTitle}. All rights reserved.`;

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navbar
        siteTitle={siteTitle}
        siteTitleHref={siteTitleHref}
        links={navLinks}
        onLinkClick={onNavLinkClick}
      />

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {children}
      </main>

      <footer className="bg-gray-800 text-gray-300" role="contentinfo">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-sm">{footerText ?? defaultFooterText}</p>
            {footerChildren && <div className="text-sm">{footerChildren}</div>}
          </div>
        </div>
      </footer>
    </div>
  );
}
