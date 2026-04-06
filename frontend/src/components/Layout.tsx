import React from 'react';
import { Link, useLocation } from 'react-router-dom';

/**
 * Props for the Layout wrapper component.
 */
interface LayoutProps {
  /** Child elements rendered in the main content area. */
  children: React.ReactNode;
}

/**
 * Application-wide layout wrapper.
 *
 * Provides a consistent header with navigation links and a footer
 * that wrap around the routed page content.
 */
const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();

  /**
   * Check if the given path matches the current location.
   */
  const isActive = (path: string): boolean => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <div className="layout" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header
        className="layout-header"
        style={{
          borderBottom: '1px solid #e2e8f0',
          padding: '0 1.5rem',
          backgroundColor: '#ffffff',
        }}
      >
        <nav
          className="layout-nav"
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            maxWidth: '1280px',
            margin: '0 auto',
            height: '64px',
          }}
          aria-label="Main navigation"
        >
          <Link
            to="/"
            className="layout-logo"
            style={{
              fontSize: '1.25rem',
              fontWeight: 700,
              textDecoration: 'none',
              color: '#1a202c',
            }}
          >
            Kanban Board
          </Link>
          <ul
            style={{
              display: 'flex',
              listStyle: 'none',
              margin: 0,
              padding: 0,
              gap: '1.5rem',
            }}
          >
            <li>
              <Link
                to="/"
                className={`nav-link${isActive('/') ? ' nav-link--active' : ''}`}
                style={{
                  textDecoration: 'none',
                  color: isActive('/') ? '#3182ce' : '#4a5568',
                  fontWeight: isActive('/') ? 600 : 400,
                }}
                aria-current={isActive('/') ? 'page' : undefined}
              >
                Boards
              </Link>
            </li>
            <li>
              <Link
                to="/categories"
                className={`nav-link${isActive('/categories') ? ' nav-link--active' : ''}`}
                style={{
                  textDecoration: 'none',
                  color: isActive('/categories') ? '#3182ce' : '#4a5568',
                  fontWeight: isActive('/categories') ? 600 : 400,
                }}
                aria-current={isActive('/categories') ? 'page' : undefined}
              >
                Categories
              </Link>
            </li>
          </ul>
        </nav>
      </header>

      <main
        className="layout-main"
        style={{
          flex: 1,
          maxWidth: '1280px',
          width: '100%',
          margin: '0 auto',
          padding: '1.5rem',
        }}
      >
        {children}
      </main>

      <footer
        className="layout-footer"
        style={{
          borderTop: '1px solid #e2e8f0',
          padding: '1.5rem',
          textAlign: 'center',
          color: '#718096',
          fontSize: '0.875rem',
          backgroundColor: '#f7fafc',
        }}
      >
        <div
          style={{
            maxWidth: '1280px',
            margin: '0 auto',
          }}
        >
          <p style={{ margin: 0 }}>
            &copy; {new Date().getFullYear()} Kanban Board. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
