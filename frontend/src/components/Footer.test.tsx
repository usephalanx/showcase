import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import Footer from './Footer';
import type { SocialLink } from './Footer';

describe('Footer', () => {
  it('renders without crashing with minimal props', () => {
    render(<Footer logoText="Maddie" />);
    const footer = screen.getByTestId('footer');
    expect(footer).toBeDefined();
  });

  it('displays the logo text', () => {
    render(<Footer logoText="Maddie Real Estate" />);
    const logo = screen.getByTestId('footer-logo');
    expect(logo.textContent).toBe('Maddie Real Estate');
  });

  it('displays the default tagline', () => {
    render(<Footer logoText="Maddie" />);
    const tagline = screen.getByTestId('footer-tagline');
    expect(tagline.textContent).toBe('Luxury real estate, personal touch.');
  });

  it('displays a custom tagline when provided', () => {
    render(<Footer logoText="Maddie" tagline="Custom tagline here." />);
    const tagline = screen.getByTestId('footer-tagline');
    expect(tagline.textContent).toBe('Custom tagline here.');
  });

  it('does not render tagline when set to empty string', () => {
    render(<Footer logoText="Maddie" tagline="" />);
    const tagline = screen.queryByTestId('footer-tagline');
    expect(tagline).toBeNull();
  });

  it('displays the default copyright text', () => {
    render(<Footer logoText="Maddie" />);
    const copyright = screen.getByTestId('footer-copyright');
    expect(copyright.textContent).toBe(
      '© 2025 Maddie Real Estate. All rights reserved.'
    );
  });

  it('displays a custom copyright text when provided', () => {
    render(<Footer logoText="Maddie" copyright="© 2024 Test Corp." />);
    const copyright = screen.getByTestId('footer-copyright');
    expect(copyright.textContent).toBe('© 2024 Test Corp.');
  });

  it('does not render copyright when set to empty string', () => {
    render(<Footer logoText="Maddie" copyright="" />);
    const copyright = screen.queryByTestId('footer-copyright');
    expect(copyright).toBeNull();
  });

  it('renders social links when provided', () => {
    const socialLinks: SocialLink[] = [
      {
        id: 'instagram',
        platform: 'Instagram',
        href: 'https://instagram.com/maddie',
        icon: React.createElement('svg', { 'data-testid': 'icon-instagram' }),
      },
      {
        id: 'facebook',
        platform: 'Facebook',
        href: 'https://facebook.com/maddie',
        icon: React.createElement('svg', { 'data-testid': 'icon-facebook' }),
      },
    ];

    render(<Footer logoText="Maddie" socialLinks={socialLinks} />);
    const container = screen.getByTestId('footer-social-icons');
    expect(container).toBeDefined();

    const igLink = screen.getByLabelText('Instagram');
    expect(igLink.getAttribute('href')).toBe('https://instagram.com/maddie');
    expect(igLink.getAttribute('target')).toBe('_blank');
    expect(igLink.getAttribute('rel')).toBe('noopener noreferrer');

    const fbLink = screen.getByLabelText('Facebook');
    expect(fbLink.getAttribute('href')).toBe('https://facebook.com/maddie');
  });

  it('does not render social icons container when no links provided', () => {
    render(<Footer logoText="Maddie" socialLinks={[]} />);
    const container = screen.queryByTestId('footer-social-icons');
    expect(container).toBeNull();
  });

  it('applies the gold top border class', () => {
    render(<Footer logoText="Maddie" />);
    const footer = screen.getByTestId('footer');
    expect(footer.className).toContain('border-t');
    expect(footer.className).toContain('border-[#C8A951]');
  });

  it('applies the dark slate background class', () => {
    render(<Footer logoText="Maddie" />);
    const footer = screen.getByTestId('footer');
    expect(footer.className).toContain('bg-slate-800');
  });

  it('applies py-8 padding', () => {
    render(<Footer logoText="Maddie" />);
    const footer = screen.getByTestId('footer');
    expect(footer.className).toContain('py-8');
  });

  it('applies additional className when provided', () => {
    render(<Footer logoText="Maddie" className="mt-10" />);
    const footer = screen.getByTestId('footer');
    expect(footer.className).toContain('mt-10');
  });

  it('tagline has italic styling', () => {
    render(<Footer logoText="Maddie" />);
    const tagline = screen.getByTestId('footer-tagline');
    expect(tagline.className).toContain('italic');
  });
});
