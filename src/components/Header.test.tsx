import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Header, { HeaderProps } from './Header';

const defaultProps: HeaderProps = {
  logoText: 'Maddie Lane',
  navLinks: [
    { label: 'About', href: '#about' },
    { label: 'Listings', href: '#listings' },
    { label: 'Contact', href: '#contact' },
  ],
  ctaText: 'Contact Maddie',
  ctaHref: '#contact',
};

describe('Header', () => {
  it('renders without crashing', () => {
    render(<Header {...defaultProps} />);
    expect(screen.getByTestId('header')).toBeInTheDocument();
  });

  it('displays the logo text from props', () => {
    render(<Header {...defaultProps} />);
    expect(screen.getByTestId('header-logo')).toHaveTextContent('Maddie Lane');
  });

  it('renders all nav links in desktop nav', () => {
    render(<Header {...defaultProps} />);
    const desktopNav = screen.getByTestId('desktop-nav');
    expect(desktopNav.querySelectorAll('a')).toHaveLength(3);
    expect(desktopNav).toHaveTextContent('About');
    expect(desktopNav).toHaveTextContent('Listings');
    expect(desktopNav).toHaveTextContent('Contact');
  });

  it('renders nav links with correct href attributes', () => {
    render(<Header {...defaultProps} />);
    const desktopNav = screen.getByTestId('desktop-nav');
    const links = desktopNav.querySelectorAll('a');
    expect(links[0]).toHaveAttribute('href', '#about');
    expect(links[1]).toHaveAttribute('href', '#listings');
    expect(links[2]).toHaveAttribute('href', '#contact');
  });

  it('renders the CTA button with correct text and href', () => {
    render(<Header {...defaultProps} />);
    const cta = screen.getByTestId('header-cta');
    expect(cta).toHaveTextContent('Contact Maddie');
    expect(cta).toHaveAttribute('href', '#contact');
  });

  it('mobile menu is collapsed by default', () => {
    render(<Header {...defaultProps} />);
    const mobileMenu = screen.getByTestId('mobile-menu');
    expect(mobileMenu).toHaveClass('max-h-0');
    expect(mobileMenu).toHaveClass('opacity-0');
  });

  it('toggles mobile menu open and closed on hamburger click', () => {
    render(<Header {...defaultProps} />);
    const button = screen.getByTestId('mobile-menu-button');
    const mobileMenu = screen.getByTestId('mobile-menu');

    // Open
    fireEvent.click(button);
    expect(mobileMenu).toHaveClass('max-h-96');
    expect(mobileMenu).toHaveClass('opacity-100');
    expect(button).toHaveAttribute('aria-expanded', 'true');

    // Close
    fireEvent.click(button);
    expect(mobileMenu).toHaveClass('max-h-0');
    expect(mobileMenu).toHaveClass('opacity-0');
    expect(button).toHaveAttribute('aria-expanded', 'false');
  });

  it('closes mobile menu when a nav link is clicked', () => {
    render(<Header {...defaultProps} />);
    const button = screen.getByTestId('mobile-menu-button');
    const mobileMenu = screen.getByTestId('mobile-menu');

    fireEvent.click(button);
    expect(mobileMenu).toHaveClass('max-h-96');

    const mobileLinks = mobileMenu.querySelectorAll('a');
    fireEvent.click(mobileLinks[0]);
    expect(mobileMenu).toHaveClass('max-h-0');
  });

  it('closes mobile menu when mobile CTA is clicked', () => {
    render(<Header {...defaultProps} />);
    const button = screen.getByTestId('mobile-menu-button');
    const mobileMenu = screen.getByTestId('mobile-menu');

    fireEvent.click(button);
    const mobileCta = screen.getByTestId('mobile-cta');
    fireEvent.click(mobileCta);
    expect(mobileMenu).toHaveClass('max-h-0');
  });

  it('applies shadow class when scrolled', () => {
    render(<Header {...defaultProps} />);
    const header = screen.getByTestId('header');

    expect(header).toHaveClass('shadow-none');

    // Simulate scroll
    Object.defineProperty(window, 'scrollY', { value: 50, writable: true });
    fireEvent.scroll(window);

    expect(header).toHaveClass('shadow-md');
  });

  it('does not hardcode logo text - uses props', () => {
    render(<Header {...defaultProps} logoText="Custom Logo" />);
    expect(screen.getByTestId('header-logo')).toHaveTextContent('Custom Logo');
  });

  it('does not hardcode CTA text - uses props', () => {
    render(<Header {...defaultProps} ctaText="Get in Touch" ctaHref="#get-in-touch" />);
    const cta = screen.getByTestId('header-cta');
    expect(cta).toHaveTextContent('Get in Touch');
    expect(cta).toHaveAttribute('href', '#get-in-touch');
  });

  it('renders with empty nav links array', () => {
    render(<Header {...defaultProps} navLinks={[]} />);
    const desktopNav = screen.getByTestId('desktop-nav');
    expect(desktopNav.querySelectorAll('a')).toHaveLength(0);
  });

  it('hamburger button has correct aria-label', () => {
    render(<Header {...defaultProps} />);
    const button = screen.getByTestId('mobile-menu-button');
    expect(button).toHaveAttribute('aria-label', 'Open menu');

    fireEvent.click(button);
    expect(button).toHaveAttribute('aria-label', 'Close menu');
  });
});
