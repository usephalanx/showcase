import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import FeaturedProperties, { Property } from './FeaturedProperties';

const makeProp = (overrides: Partial<Property> = {}): Property => ({
  id: '1',
  title: 'Luxury Villa',
  slug: 'luxury-villa',
  price: 1250000,
  address: '123 Ocean Drive',
  city: 'Miami',
  state: 'FL',
  zipCode: '33101',
  propertyType: 'house',
  bedrooms: 4,
  bathrooms: 3,
  squareFeet: 3200,
  description: 'A beautiful luxury villa on the waterfront.',
  features: ['Pool', 'Garage'],
  images: ['https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop'],
  listingDate: '2024-01-15',
  status: 'for-sale',
  featured: true,
  ...overrides,
});

const sampleProperties: Property[] = [
  makeProp({ id: '1', title: 'Luxury Villa', featured: true }),
  makeProp({ id: '2', title: 'Downtown Condo', featured: false, propertyType: 'condo', price: 450000 }),
  makeProp({ id: '3', title: 'Beach House', featured: true, price: 890000 }),
  makeProp({ id: '4', title: 'Suburban Home', featured: false, price: 320000 }),
];

describe('FeaturedProperties', () => {
  it('renders without crashing', () => {
    render(<FeaturedProperties properties={[]} />);
    expect(screen.getByText('Featured Properties')).toBeInTheDocument();
  });

  it('displays the default heading and view all link', () => {
    render(<FeaturedProperties properties={[]} />);
    expect(screen.getByRole('heading', { name: 'Featured Properties' })).toBeInTheDocument();
    expect(screen.getByText('View All Properties')).toBeInTheDocument();
  });

  it('displays a custom heading when provided', () => {
    render(<FeaturedProperties properties={[]} heading="Hot Listings" />);
    expect(screen.getByRole('heading', { name: 'Hot Listings' })).toBeInTheDocument();
  });

  it('displays a subheading when provided', () => {
    render(<FeaturedProperties properties={[]} subheading="Hand-picked for you" />);
    expect(screen.getByText('Hand-picked for you')).toBeInTheDocument();
  });

  it('filters and displays only featured properties', () => {
    render(<FeaturedProperties properties={sampleProperties} />);
    expect(screen.getByText('Luxury Villa')).toBeInTheDocument();
    expect(screen.getByText('Beach House')).toBeInTheDocument();
    expect(screen.queryByText('Downtown Condo')).not.toBeInTheDocument();
    expect(screen.queryByText('Suburban Home')).not.toBeInTheDocument();
  });

  it('shows empty state when no properties are featured', () => {
    const nonFeatured = sampleProperties.map((p) => ({ ...p, featured: false }));
    render(<FeaturedProperties properties={nonFeatured} />);
    expect(screen.getByTestId('no-featured')).toBeInTheDocument();
    expect(screen.getByText('No featured properties available at this time.')).toBeInTheDocument();
  });

  it('renders the property grid with correct number of cards', () => {
    render(<FeaturedProperties properties={sampleProperties} />);
    const grid = screen.getByTestId('property-grid');
    const cards = grid.querySelectorAll('.featured-property-card');
    expect(cards.length).toBe(2);
  });

  it('displays formatted price on property cards', () => {
    render(<FeaturedProperties properties={sampleProperties} />);
    expect(screen.getByText('$1,250,000')).toBeInTheDocument();
    expect(screen.getByText('$890,000')).toBeInTheDocument();
  });

  it('displays property details (beds, baths, sqft)', () => {
    render(<FeaturedProperties properties={[makeProp({ bedrooms: 5, bathrooms: 4, squareFeet: 4500 })]} />);
    expect(screen.getByText('5 Beds')).toBeInTheDocument();
    expect(screen.getByText('4 Baths')).toBeInTheDocument();
    expect(screen.getByText('4,500 Sq Ft')).toBeInTheDocument();
  });

  it('displays property address', () => {
    render(<FeaturedProperties properties={sampleProperties} />);
    expect(screen.getByText('123 Ocean Drive, Miami, FL 33101')).toBeInTheDocument();
  });

  it('renders a button with onViewAll callback when provided', () => {
    const handleViewAll = vi.fn();
    render(<FeaturedProperties properties={sampleProperties} onViewAll={handleViewAll} />);
    const button = screen.getByRole('button', { name: 'View All Properties' });
    fireEvent.click(button);
    expect(handleViewAll).toHaveBeenCalledTimes(1);
  });

  it('renders a link when no onViewAll is provided', () => {
    render(<FeaturedProperties properties={sampleProperties} viewAllHref="/listings" />);
    const link = screen.getByRole('link', { name: 'View All Properties' });
    expect(link).toHaveAttribute('href', '/listings');
  });

  it('uses custom viewAllLabel', () => {
    render(<FeaturedProperties properties={sampleProperties} viewAllLabel="Browse Listings" />);
    expect(screen.getByText('Browse Listings')).toBeInTheDocument();
  });

  it('fires onPropertyClick when a card is clicked', () => {
    const handleClick = vi.fn();
    render(<FeaturedProperties properties={sampleProperties} onPropertyClick={handleClick} />);
    const card = screen.getByText('Luxury Villa').closest('.featured-property-card')!;
    fireEvent.click(card);
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith(expect.objectContaining({ id: '1', title: 'Luxury Villa' }));
  });

  it('renders decorative elements', () => {
    render(<FeaturedProperties properties={[]} />);
    expect(screen.getByText('★')).toBeInTheDocument();
  });

  it('has accessible section with aria-labelledby', () => {
    render(<FeaturedProperties properties={[]} />);
    const section = screen.getByRole('region', { name: 'Featured Properties' });
    expect(section).toBeInTheDocument();
  });

  it('each property card has the correct article role', () => {
    render(<FeaturedProperties properties={sampleProperties} />);
    const articles = screen.getAllByRole('article');
    expect(articles.length).toBe(2);
    expect(articles[0]).toHaveAttribute('aria-label', 'Luxury Villa');
  });
});
