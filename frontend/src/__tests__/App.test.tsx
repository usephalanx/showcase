import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '../App';

describe('App', () => {
  it('renders the Logo component', () => {
    render(<App />);
    expect(screen.getByTestId('logo')).toBeInTheDocument();
  });

  it('renders the CompanyName component', () => {
    render(<App />);
    expect(screen.getByTestId('company-name')).toBeInTheDocument();
  });

  it('renders the Profile component', () => {
    render(<App />);
    expect(screen.getByTestId('profile')).toBeInTheDocument();
  });

  it('renders the RecentSales component', () => {
    render(<App />);
    expect(screen.getByTestId('recent-sales')).toBeInTheDocument();
  });

  it('renders the ContactInfo component', () => {
    render(<App />);
    expect(screen.getByTestId('contact-info')).toBeInTheDocument();
  });

  it('renders all sections in correct order', () => {
    const { container } = render(<App />);

    const header = container.querySelector('.app-header');
    const main = container.querySelector('.app-main');

    expect(header).toBeInTheDocument();
    expect(main).toBeInTheDocument();

    // Logo and CompanyName should be in the header
    expect(header!.querySelector('[data-testid="logo"]')).toBeInTheDocument();
    expect(header!.querySelector('[data-testid="company-name"]')).toBeInTheDocument();

    // Profile, RecentSales, ContactInfo should be in main
    const mainChildren = main!.children;
    expect(mainChildren[0]).toHaveAttribute('data-testid', 'profile');
    expect(mainChildren[1]).toHaveAttribute('data-testid', 'recent-sales');
    expect(mainChildren[2]).toHaveAttribute('data-testid', 'contact-info');
  });

  it('renders the footer with copyright', () => {
    render(<App />);
    const year = new Date().getFullYear().toString();
    expect(screen.getByText(new RegExp(year))).toBeInTheDocument();
  });
});
