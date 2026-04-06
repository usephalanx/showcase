import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import HeroSection, { HeroSectionProps } from './HeroSection';

const defaultProps: HeroSectionProps = {
  headline: 'Find Your Dream Home',
  subheading: 'Discover luxury properties in the most sought-after neighborhoods.',
  backgroundImageUrl:
    'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1600&h=900&fit=crop',
};

describe('HeroSection', () => {
  it('renders without crashing', () => {
    render(<HeroSection {...defaultProps} />);
    expect(screen.getByTestId('hero-section')).toBeTruthy();
  });

  it('displays the headline text', () => {
    render(<HeroSection {...defaultProps} />);
    expect(screen.getByTestId('hero-headline').textContent).toBe(
      'Find Your Dream Home'
    );
  });

  it('displays the subheading text', () => {
    render(<HeroSection {...defaultProps} />);
    expect(screen.getByTestId('hero-subheading').textContent).toBe(
      'Discover luxury properties in the most sought-after neighborhoods.'
    );
  });

  it('renders the background image with the correct URL', () => {
    render(<HeroSection {...defaultProps} />);
    const bg = screen.getByTestId('hero-background');
    expect(bg.style.backgroundImage).toContain(defaultProps.backgroundImageUrl);
  });

  it('renders the dark overlay', () => {
    render(<HeroSection {...defaultProps} />);
    expect(screen.getByTestId('hero-overlay')).toBeTruthy();
  });

  it('uses custom overlay opacity when provided', () => {
    render(<HeroSection {...defaultProps} overlayOpacity={0.7} />);
    const overlay = screen.getByTestId('hero-overlay');
    expect(overlay.style.backgroundColor).toBe('rgba(0, 0, 0, 0.7)');
  });

  it('renders the search form with default placeholder', () => {
    render(<HeroSection {...defaultProps} />);
    const input = screen.getByTestId('hero-search-input') as HTMLInputElement;
    expect(input.placeholder).toBe(
      'Search by city, neighborhood, or ZIP...'
    );
  });

  it('renders custom search placeholder', () => {
    render(
      <HeroSection {...defaultProps} searchPlaceholder="Enter an address..." />
    );
    const input = screen.getByTestId('hero-search-input') as HTMLInputElement;
    expect(input.placeholder).toBe('Enter an address...');
  });

  it('renders the CTA button with default label', () => {
    render(<HeroSection {...defaultProps} />);
    expect(screen.getByTestId('hero-cta-button').textContent).toBe('Search');
  });

  it('renders a custom CTA button label', () => {
    render(<HeroSection {...defaultProps} ctaButtonLabel="Explore" />);
    expect(screen.getByTestId('hero-cta-button').textContent).toBe('Explore');
  });

  it('calls onSearch with the input value when the form is submitted', () => {
    const onSearch = vi.fn();
    render(<HeroSection {...defaultProps} onSearch={onSearch} />);

    const input = screen.getByTestId('hero-search-input');
    fireEvent.change(input, { target: { value: 'Beverly Hills' } });

    const form = screen.getByTestId('hero-search-form');
    fireEvent.submit(form);

    expect(onSearch).toHaveBeenCalledTimes(1);
    expect(onSearch).toHaveBeenCalledWith('Beverly Hills');
  });

  it('does not throw when submitted without an onSearch handler', () => {
    render(<HeroSection {...defaultProps} />);
    const form = screen.getByTestId('hero-search-form');
    expect(() => fireEvent.submit(form)).not.toThrow();
  });

  it('applies the custom minHeight', () => {
    render(<HeroSection {...defaultProps} minHeight="80vh" />);
    const section = screen.getByTestId('hero-section');
    expect(section.style.minHeight).toBe('80vh');
  });

  it('defaults minHeight to 70vh', () => {
    render(<HeroSection {...defaultProps} />);
    const section = screen.getByTestId('hero-section');
    expect(section.style.minHeight).toBe('70vh');
  });

  it('updates search input value when user types', () => {
    render(<HeroSection {...defaultProps} />);
    const input = screen.getByTestId('hero-search-input') as HTMLInputElement;
    fireEvent.change(input, { target: { value: 'Malibu' } });
    expect(input.value).toBe('Malibu');
  });
});
