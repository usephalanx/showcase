import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import PropertyCard, { PropertyCardProps } from './PropertyCard';

const defaultProps: PropertyCardProps = {
  imageUrl: 'https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800',
  address: '123 Maple Street, Beverly Hills, CA 90210',
  price: '$1.2M',
  status: 'SOLD',
};

describe('PropertyCard', () => {
  it('renders without crashing', () => {
    const { container } = render(<PropertyCard {...defaultProps} />);
    expect(container).toBeTruthy();
  });

  it('renders the property card container', () => {
    render(<PropertyCard {...defaultProps} />);
    const card = screen.getByTestId('property-card');
    expect(card).toBeDefined();
  });

  it('displays the property image with correct src and alt', () => {
    render(<PropertyCard {...defaultProps} />);
    const img = screen.getByRole('img');
    expect(img.getAttribute('src')).toBe(defaultProps.imageUrl);
    expect(img.getAttribute('alt')).toBe(defaultProps.address);
  });

  it('uses custom imageAlt when provided', () => {
    render(<PropertyCard {...defaultProps} imageAlt="Beautiful home" />);
    const img = screen.getByRole('img');
    expect(img.getAttribute('alt')).toBe('Beautiful home');
  });

  it('displays the SOLD status badge', () => {
    render(<PropertyCard {...defaultProps} />);
    const badge = screen.getByTestId('status-badge');
    expect(badge.textContent).toBe('SOLD');
  });

  it('styles the badge with dark background and gold text', () => {
    render(<PropertyCard {...defaultProps} />);
    const badge = screen.getByTestId('status-badge');
    expect(badge.style.backgroundColor).toBe('rgb(30, 41, 59)');
    expect(badge.style.color).toBe('rgb(200, 169, 81)');
  });

  it('displays the address', () => {
    render(<PropertyCard {...defaultProps} />);
    const address = screen.getByTestId('property-address');
    expect(address.textContent).toBe(defaultProps.address);
  });

  it('displays the price in bold', () => {
    render(<PropertyCard {...defaultProps} />);
    const price = screen.getByTestId('property-price');
    expect(price.textContent).toBe(defaultProps.price);
    expect(price.className).toContain('font-bold');
  });

  it('renders with different prop values', () => {
    const customProps: PropertyCardProps = {
      imageUrl: 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800',
      address: '456 Oak Avenue, Malibu, CA 90265',
      price: '$3.5M',
      status: 'SOLD',
    };
    render(<PropertyCard {...customProps} />);
    expect(screen.getByTestId('property-address').textContent).toBe(customProps.address);
    expect(screen.getByTestId('property-price').textContent).toBe(customProps.price);
    expect(screen.getByRole('img').getAttribute('src')).toBe(customProps.imageUrl);
  });

  it('has hover-related transition classes on the card', () => {
    render(<PropertyCard {...defaultProps} />);
    const card = screen.getByTestId('property-card');
    expect(card.className).toContain('hover:shadow-xl');
    expect(card.className).toContain('hover:scale-');
    expect(card.className).toContain('transition-all');
  });

  it('has rounded overflow-hidden styling', () => {
    render(<PropertyCard {...defaultProps} />);
    const card = screen.getByTestId('property-card');
    expect(card.className).toContain('rounded-xl');
    expect(card.className).toContain('overflow-hidden');
  });

  it('sets lazy loading on the image', () => {
    render(<PropertyCard {...defaultProps} />);
    const img = screen.getByRole('img');
    expect(img.getAttribute('loading')).toBe('lazy');
  });
});
