import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import RecentSales from './RecentSales';
import type { PropertyCardData } from './RecentSales';

describe('RecentSales', () => {
  it('renders without crashing', () => {
    const { container } = render(<RecentSales />);
    expect(container).toBeTruthy();
  });

  it('renders the default section heading', () => {
    render(<RecentSales />);
    const heading = screen.getByTestId('section-heading');
    expect(heading.textContent).toBe('Recent Sales');
  });

  it('renders with a custom heading', () => {
    render(<RecentSales heading="Featured Properties" />);
    const heading = screen.getByTestId('section-heading');
    expect(heading.textContent).toBe('Featured Properties');
  });

  it('renders the section with the correct id', () => {
    const { container } = render(<RecentSales sectionId="my-listings" />);
    const section = container.querySelector('#my-listings');
    expect(section).toBeTruthy();
  });

  it('renders the default id "listings"', () => {
    const { container } = render(<RecentSales />);
    const section = container.querySelector('#listings');
    expect(section).toBeTruthy();
  });

  it('renders 3 property cards by default', () => {
    render(<RecentSales />);
    const cards = screen.getAllByTestId('property-card');
    expect(cards).toHaveLength(3);
  });

  it('renders correct default addresses', () => {
    render(<RecentSales />);
    const addresses = screen.getAllByTestId('property-address');
    expect(addresses[0].textContent).toBe('742 Evergreen Terrace, Beverly Hills');
    expect(addresses[1].textContent).toBe('1201 Ocean Avenue, Malibu');
    expect(addresses[2].textContent).toBe('88 Sunset Boulevard, Pacific Palisades');
  });

  it('renders correct default prices', () => {
    render(<RecentSales />);
    const prices = screen.getAllByTestId('property-price');
    expect(prices[0].textContent).toBe('$1.2M');
    expect(prices[1].textContent).toBe('$875K');
    expect(prices[2].textContent).toBe('$2.1M');
  });

  it('marks all default properties as SOLD', () => {
    render(<RecentSales />);
    const statuses = screen.getAllByTestId('property-status');
    expect(statuses).toHaveLength(3);
    statuses.forEach((badge) => {
      expect(badge.textContent).toBe('SOLD');
    });
  });

  it('renders custom properties when provided', () => {
    const customProperties: PropertyCardData[] = [
      {
        imageUrl: 'https://example.com/img1.jpg',
        address: '123 Main St',
        price: '$500K',
        status: 'FOR SALE',
      },
    ];
    render(<RecentSales properties={customProperties} />);
    const cards = screen.getAllByTestId('property-card');
    expect(cards).toHaveLength(1);
    expect(screen.getByTestId('property-address').textContent).toBe('123 Main St');
    expect(screen.getByTestId('property-price').textContent).toBe('$500K');
    expect(screen.getByTestId('property-status').textContent).toBe('FOR SALE');
  });

  it('renders property images with correct src and alt', () => {
    render(<RecentSales />);
    const images = screen.getAllByRole('img');
    expect(images).toHaveLength(3);
    expect(images[0]).toHaveAttribute('alt', '742 Evergreen Terrace, Beverly Hills');
    expect(images[0]).toHaveAttribute(
      'src',
      'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800&q=80'
    );
  });

  it('applies Playfair Display font to heading', () => {
    render(<RecentSales />);
    const heading = screen.getByTestId('section-heading');
    expect(heading.style.fontFamily).toContain('Playfair Display');
  });

  it('renders an empty grid when given an empty properties array', () => {
    render(<RecentSales properties={[]} />);
    const cards = screen.queryAllByTestId('property-card');
    expect(cards).toHaveLength(0);
  });
});
