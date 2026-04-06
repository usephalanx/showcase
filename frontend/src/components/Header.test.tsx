import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Header, { HeaderProps } from './Header';

const defaultProps: HeaderProps = {
  brandName: 'Prestige Realty',
  navLinks: [
    { label: 'Home', href: '/' },
    { label: 'Properties', href: '/properties' },
    { label: 'Contact', href: '/contact' },
  ],
};

describe('Header', () => {
  it('renders without crashing', () => {
    render(<Header {...defaultProps} />);
    expect(screen.getByTestId('header')).toBeInTheDocument();
  });

  it('displays the brand name', () => {
    render(<Header {...defaultProps} />);
    expect(screen.getByTestId('brand-name')).toHaveTextContent('Prestige Realty');
  });

  it('renders all navigation links in desktop nav', () => {
    render(<Header {...defaultProps} />);
    const desktopNav = screen.getByTestId('desktop-nav');
    expect(desktopNav).toBeInTheDocument();
    defaultProps.navLinks.forEach((link) => {
      expect(desktopNav).toHaveTextContent(link.label);
    });
  });

  it('shows the hamburger button for mobile', () => {
    render(<Header {...defaultProps} />);
    expect(screen.getByTestId('hamburger-button')).toBeInTheDocument();
  });

  it('opens mobile drawer when hamburger is clicked', () => {
    render(<Header {...defaultProps} />);
    const hamburger = screen.getByTestId('hamburger-button');
    fireEvent.click(hamburger);
    const drawer = screen.getByTestId('mobile-drawer');
    expect(drawer.className).toContain('translate-x-0');
  });

  it('closes mobile drawer when close button is clicked', () => {
    render(<Header {...defaultProps} />);
    fireEvent.click(screen.getByTestId('hamburger-button'));
    fireEvent.click(screen.getByTestId('close-drawer-button'));
    const drawer = screen.getByTestId('mobile-drawer');
    expect(drawer.className).toContain('translate-x-full');
  });

  it('closes mobile drawer when overlay is clicked', () => {
    render(<Header {...defaultProps} />);
    fireEvent.click(screen.getByTestId('hamburger-button'));
    fireEvent.click(screen.getByTestId('drawer-overlay'));
    const drawer = screen.getByTestId('mobile-drawer');
    expect(drawer.className).toContain('translate-x-full');
  });

  it('calls onNavigate when a nav link is clicked', () => {
    const onNavigate = vi.fn();
    render(<Header {...defaultProps} onNavigate={onNavigate} />);
    const desktopNav = screen.getByTestId('desktop-nav');
    const homeButton = desktopNav.querySelector('button');
    fireEvent.click(homeButton!);
    expect(onNavigate).toHaveBeenCalledWith('/');
  });

  it('calls onNavigate when brand name is clicked', () => {
    const onNavigate = vi.fn();
    render(<Header {...defaultProps} onNavigate={onNavigate} />);
    fireEvent.click(screen.getByTestId('brand-name'));
    expect(onNavigate).toHaveBeenCalledWith('/');
  });

  it('applies solid background class when scrolled', () => {
    render(<Header {...defaultProps} />);
    // Simulate scroll
    Object.defineProperty(window, 'scrollY', { value: 100, writable: true });
    fireEvent.scroll(window);
    const header = screen.getByTestId('header');
    expect(header.className).toContain('bg-white');
  });
});
