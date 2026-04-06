import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import PropertyCard, { PropertyCardProps } from './PropertyCard';
import { Property } from '../types/models';

const mockAgent = {
  id: 'agent-1',
  name: 'Jane Smith',
  title: 'Senior Agent',
  phone: '555-0100',
  email: 'jane@example.com',
  photo: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop',
  bio: 'Experienced real estate agent.',
  specialties: ['Residential', 'Luxury'],
  propertiesCount: 42,
  rating: 4.9,
  socialLinks: {},
};

const createMockProperty = (overrides: Partial<Property> = {}): Property => ({
  id: 'prop-1',
  title: 'Modern Luxury Villa',
  slug: 'modern-luxury-villa',
  price: 1250000,
  address: '123 Elm Street',
  city: 'Austin',
  state: 'TX',
  zipCode: '78701',
  propertyType: 'house',
  bedrooms: 4,
  bathrooms: 3,
  squareFeet: 2800,
  lotSize: 0.35,
  yearBuilt: 2021,
  description: 'A beautiful modern villa.',
  features: ['Pool', 'Garage', 'Smart Home'],
  images: [
    'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop',
    'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
  ],
  agent: mockAgent,
  neighborhood: 'downtown',
  listingDate: '2024-01-15',
  status: 'for-sale',
  isFeatured: false,
  ...overrides,
});

const renderCard = (props: Partial<PropertyCardProps> = {}) => {
  const defaultProps: PropertyCardProps = {
    property: createMockProperty(),
    ...props,
  };
  return render(<PropertyCard {...defaultProps} />);
};

describe('PropertyCard', () => {
  it('renders without crashing', () => {
    renderCard();
    expect(screen.getByTestId('property-card')).toBeInTheDocument();
  });

  it('displays the formatted price with commas', () => {
    renderCard({ property: createMockProperty({ price: 1250000 }) });
    expect(screen.getByTestId('property-price')).toHaveTextContent('$1,250,000');
  });

  it('displays the full address', () => {
    renderCard();
    expect(screen.getByTestId('property-address')).toHaveTextContent(
      '123 Elm Street, Austin, TX 78701'
    );
  });

  it('displays bedrooms count', () => {
    renderCard({ property: createMockProperty({ bedrooms: 4 }) });
    expect(screen.getByTestId('property-beds')).toHaveTextContent('4');
  });

  it('displays bathrooms count', () => {
    renderCard({ property: createMockProperty({ bathrooms: 3 }) });
    expect(screen.getByTestId('property-baths')).toHaveTextContent('3');
  });

  it('displays formatted square feet', () => {
    renderCard({ property: createMockProperty({ squareFeet: 2800 }) });
    expect(screen.getByTestId('property-sqft')).toHaveTextContent('2,800');
  });

  it('shows Featured badge when isFeatured is true', () => {
    renderCard({ property: createMockProperty({ isFeatured: true }) });
    expect(screen.getByTestId('featured-badge')).toBeInTheDocument();
    expect(screen.getByTestId('featured-badge')).toHaveTextContent('Featured');
  });

  it('does not show Featured badge when isFeatured is false', () => {
    renderCard({ property: createMockProperty({ isFeatured: false }) });
    expect(screen.queryByTestId('featured-badge')).not.toBeInTheDocument();
  });

  it('displays the correct status badge for "for-sale"', () => {
    renderCard({ property: createMockProperty({ status: 'for-sale' }) });
    expect(screen.getByTestId('status-badge')).toHaveTextContent('For Sale');
  });

  it('displays the correct status badge for "pending"', () => {
    renderCard({ property: createMockProperty({ status: 'pending' }) });
    expect(screen.getByTestId('status-badge')).toHaveTextContent('Pending');
  });

  it('displays the correct status badge for "sold"', () => {
    renderCard({ property: createMockProperty({ status: 'sold' }) });
    expect(screen.getByTestId('status-badge')).toHaveTextContent('Sold');
  });

  it('renders the primary image with object-cover and correct alt text', () => {
    renderCard();
    const img = screen.getByAlt('Modern Luxury Villa');
    expect(img).toBeInTheDocument();
    expect(img).toHaveAttribute(
      'src',
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop'
    );
    expect(img.className).toContain('object-cover');
  });

  it('calls onViewDetail with the slug when clicked', () => {
    const handleViewDetail = vi.fn();
    renderCard({
      property: createMockProperty({ slug: 'modern-luxury-villa' }),
      onViewDetail: handleViewDetail,
    });
    fireEvent.click(screen.getByTestId('property-card'));
    expect(handleViewDetail).toHaveBeenCalledTimes(1);
    expect(handleViewDetail).toHaveBeenCalledWith('modern-luxury-villa');
  });

  it('calls onViewDetail when Enter key is pressed', () => {
    const handleViewDetail = vi.fn();
    renderCard({
      property: createMockProperty({ slug: 'test-property' }),
      onViewDetail: handleViewDetail,
    });
    fireEvent.keyDown(screen.getByTestId('property-card'), { key: 'Enter' });
    expect(handleViewDetail).toHaveBeenCalledTimes(1);
    expect(handleViewDetail).toHaveBeenCalledWith('test-property');
  });

  it('does not crash when onViewDetail is not provided', () => {
    renderCard({ onViewDetail: undefined });
    expect(() => {
      fireEvent.click(screen.getByTestId('property-card'));
    }).not.toThrow();
  });

  it('handles property with no images gracefully', () => {
    renderCard({ property: createMockProperty({ images: [] }) });
    expect(screen.getByTestId('property-card')).toBeInTheDocument();
    expect(screen.queryByRole('img')).not.toBeInTheDocument();
  });

  it('applies custom className', () => {
    renderCard({ className: 'my-custom-class' });
    expect(screen.getByTestId('property-card').className).toContain('my-custom-class');
  });

  it('has proper accessibility attributes', () => {
    renderCard();
    const card = screen.getByTestId('property-card');
    expect(card).toHaveAttribute('role', 'link');
    expect(card).toHaveAttribute('tabindex', '0');
    expect(card).toHaveAttribute(
      'aria-label',
      'View details for Modern Luxury Villa'
    );
  });

  it('formats large prices correctly', () => {
    renderCard({ property: createMockProperty({ price: 15999999 }) });
    expect(screen.getByTestId('property-price')).toHaveTextContent('$15,999,999');
  });

  it('formats large square footage correctly', () => {
    renderCard({ property: createMockProperty({ squareFeet: 12500 }) });
    expect(screen.getByTestId('property-sqft')).toHaveTextContent('12,500');
  });
});
