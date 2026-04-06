import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Footer, { FooterProps } from './Footer';

const defaultProps: FooterProps = {
  brandName: 'Prestige Realty',
  brandDescription: 'Your trusted partner in luxury real estate.',
  quickLinks: [
    { label: 'Home', href: '/' },
    { label: 'Properties', href: '/properties' },
    { label: 'Contact', href: '/contact' },
  ],
  contactInfo: {
    address: '123 Main Street, Beverly Hills, CA 90210',
    phone: '(555) 123-4567',
    email: 'info@prestigerealty.com',
  },
  socialLinks: [
    {
      platform: 'Facebook',
      href: 'https://facebook.com',
      iconPath:
        'M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z',
    },
    {
      platform: 'Twitter',
      href: 'https://twitter.com',
      iconPath:
        'M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z',
    },
  ],
  copyrightYear: 2024,
};

describe('Footer', () => {
  it('renders without crashing', () => {
    render(<Footer {...defaultProps} />);
    expect(screen.getByTestId('footer')).toBeInTheDocument();
  });

  it('displays the brand name and description', () => {
    render(<Footer {...defaultProps} />);
    const brand = screen.getByTestId('footer-brand');
    expect(brand).toHaveTextContent('Prestige Realty');
    expect(brand).toHaveTextContent('Your trusted partner in luxury real estate.');
  });

  it('renders all quick links', () => {
    render(<Footer {...defaultProps} />);
    const quickLinks = screen.getByTestId('footer-quick-links');
    defaultProps.quickLinks.forEach((link) => {
      expect(quickLinks).toHaveTextContent(link.label);
    });
  });

  it('renders contact information', () => {
    render(<Footer {...defaultProps} />);
    const contact = screen.getByTestId('footer-contact');
    expect(contact).toHaveTextContent('123 Main Street, Beverly Hills, CA 90210');
    expect(contact).toHaveTextContent('(555) 123-4567');
    expect(contact).toHaveTextContent('info@prestigerealty.com');
  });

  it('renders social media links', () => {
    render(<Footer {...defaultProps} />);
    const social = screen.getByTestId('footer-social');
    expect(social).toBeInTheDocument();
    const links = social.querySelectorAll('a');
    expect(links).toHaveLength(2);
    expect(links[0]).toHaveAttribute('href', 'https://facebook.com');
    expect(links[0]).toHaveAttribute('aria-label', 'Facebook');
    expect(links[1]).toHaveAttribute('href', 'https://twitter.com');
    expect(links[1]).toHaveAttribute('aria-label', 'Twitter');
  });

  it('renders social links with target _blank and rel attributes', () => {
    render(<Footer {...defaultProps} />);
    const social = screen.getByTestId('footer-social');
    const links = social.querySelectorAll('a');
    links.forEach((link) => {
      expect(link).toHaveAttribute('target', '_blank');
      expect(link).toHaveAttribute('rel', 'noopener noreferrer');
    });
  });

  it('displays copyright with year and brand name', () => {
    render(<Footer {...defaultProps} />);
    const copyright = screen.getByTestId('footer-copyright');
    expect(copyright).toHaveTextContent('© 2024 Prestige Realty. All rights reserved.');
  });

  it('calls onNavigate when a quick link is clicked', () => {
    const onNavigate = vi.fn();
    render(<Footer {...defaultProps} onNavigate={onNavigate} />);
    const quickLinks = screen.getByTestId('footer-quick-links');
    const buttons = quickLinks.querySelectorAll('button');
    fireEvent.click(buttons[1]);
    expect(onNavigate).toHaveBeenCalledWith('/properties');
  });

  it('renders with different props without crashing', () => {
    render(
      <Footer
        {...defaultProps}
        brandName="Other Realty"
        copyrightYear={2025}
      />
    );
    expect(screen.getByTestId('footer-brand')).toHaveTextContent('Other Realty');
    expect(screen.getByTestId('footer-copyright')).toHaveTextContent('2025');
  });
});
