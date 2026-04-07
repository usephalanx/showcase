import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Hero, { HeroProps } from './Hero';

const defaultProps: HeroProps = {
  headline: 'Your Dream Home Starts Here',
  subheading: 'Luxury real estate tailored to your lifestyle.',
  backgroundImageUrl:
    'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9',
  primaryCtaLabel: 'View My Listings',
  primaryCtaHref: '#listings',
  secondaryCtaLabel: 'Get In Touch',
  secondaryCtaHref: '#contact',
};

describe('Hero', () => {
  it('renders without crashing', () => {
    const { container } = render(<Hero {...defaultProps} />);
    expect(container).toBeTruthy();
  });

  it('displays the headline text', () => {
    render(<Hero {...defaultProps} />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading.textContent).toBe('Your Dream Home Starts Here');
  });

  it('displays the subheading text', () => {
    render(<Hero {...defaultProps} />);
    expect(screen.getByText('Luxury real estate tailored to your lifestyle.')).toBeTruthy();
  });

  it('renders the primary CTA with correct href', () => {
    render(<Hero {...defaultProps} />);
    const primaryLink = screen.getByText('View My Listings');
    expect(primaryLink.tagName).toBe('A');
    expect(primaryLink.getAttribute('href')).toBe('#listings');
  });

  it('renders the secondary CTA with correct href', () => {
    render(<Hero {...defaultProps} />);
    const secondaryLink = screen.getByText('Get In Touch');
    expect(secondaryLink.tagName).toBe('A');
    expect(secondaryLink.getAttribute('href')).toBe('#contact');
  });

  it('applies the background image URL as inline style', () => {
    render(<Hero {...defaultProps} />);
    const section = screen.getByRole('banner');
    expect(section.style.backgroundImage).toContain(
      'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9'
    );
  });

  it('uses the default aria-label when backgroundAlt is not provided', () => {
    render(<Hero {...defaultProps} />);
    const section = screen.getByRole('banner');
    expect(section.getAttribute('aria-label')).toBe('Luxury home exterior');
  });

  it('uses a custom backgroundAlt when provided', () => {
    render(<Hero {...defaultProps} backgroundAlt="Beautiful mansion" />);
    const section = screen.getByRole('banner');
    expect(section.getAttribute('aria-label')).toBe('Beautiful mansion');
  });

  it('renders the overlay div for text readability', () => {
    const { container } = render(<Hero {...defaultProps} />);
    const overlay = container.querySelector('[aria-hidden="true"]');
    expect(overlay).toBeTruthy();
    expect(overlay!.getAttribute('style')).toContain('linear-gradient');
  });

  it('renders with custom headline and subheading props', () => {
    render(
      <Hero
        {...defaultProps}
        headline="Find Your Paradise"
        subheading="We make it happen."
      />
    );
    expect(screen.getByText('Find Your Paradise')).toBeTruthy();
    expect(screen.getByText('We make it happen.')).toBeTruthy();
  });

  it('renders both CTA buttons as links', () => {
    render(<Hero {...defaultProps} />);
    const links = screen.getAllByRole('link');
    expect(links.length).toBe(2);
  });
});
