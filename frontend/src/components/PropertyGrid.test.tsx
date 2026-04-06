import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import PropertyGrid, { PropertyGridItem } from './PropertyGrid';

// Mock PropertyCard so we isolate PropertyGrid logic
vi.mock('./PropertyCard', () => ({
  default: (props: {
    id: string;
    title: string;
    price: number;
    address: string;
    city: string;
    state: string;
    zipCode: string;
    propertyType: string;
    bedrooms: number;
    bathrooms: number;
    squareFeet: number;
    image: string;
    status: string;
    onClick?: () => void;
  }) => (
    <div data-testid={`property-card-${props.id}`} onClick={props.onClick}>
      <span data-testid="card-title">{props.title}</span>
      <span data-testid="card-price">{props.price}</span>
    </div>
  ),
}));

const createMockProperty = (overrides: Partial<PropertyGridItem> = {}): PropertyGridItem => ({
  id: '1',
  title: 'Beautiful Family Home',
  slug: 'beautiful-family-home',
  price: 450000,
  address: '123 Main St',
  city: 'Springfield',
  state: 'IL',
  zipCode: '62701',
  propertyType: 'house',
  bedrooms: 4,
  bathrooms: 3,
  squareFeet: 2500,
  lotSize: '0.5 acres',
  yearBuilt: 2010,
  description: 'A wonderful home for the whole family.',
  features: ['Garage', 'Pool', 'Garden'],
  images: ['https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop'],
  listingDate: '2024-01-15',
  status: 'for-sale',
  ...overrides,
});

const sampleProperties: PropertyGridItem[] = [
  createMockProperty({ id: '1', title: 'Home One', price: 300000 }),
  createMockProperty({ id: '2', title: 'Home Two', price: 450000 }),
  createMockProperty({ id: '3', title: 'Home Three', price: 600000 }),
];

describe('PropertyGrid', () => {
  it('renders without crashing', () => {
    render(
      <PropertyGrid properties={[]} emptyMessage="No properties found." />
    );
    expect(screen.getByTestId('property-grid')).toBeInTheDocument();
  });

  it('displays the section title when provided', () => {
    render(
      <PropertyGrid
        properties={sampleProperties}
        title="Featured Listings"
        emptyMessage="No properties found."
      />
    );
    expect(screen.getByText('Featured Listings')).toBeInTheDocument();
    expect(screen.getByTestId('property-grid-header')).toBeInTheDocument();
  });

  it('renders the decorative underline when title is provided', () => {
    render(
      <PropertyGrid
        properties={sampleProperties}
        title="Our Properties"
        emptyMessage="No properties found."
      />
    );
    expect(screen.getByTestId('property-grid-underline')).toBeInTheDocument();
  });

  it('does not render header when title is not provided', () => {
    render(
      <PropertyGrid properties={sampleProperties} emptyMessage="No properties found." />
    );
    expect(screen.queryByTestId('property-grid-header')).not.toBeInTheDocument();
  });

  it('shows emptyMessage when properties array is empty', () => {
    const emptyMsg = 'No properties match your criteria.';
    render(<PropertyGrid properties={[]} emptyMessage={emptyMsg} />);
    expect(screen.getByTestId('property-grid-empty')).toBeInTheDocument();
    expect(screen.getByText(emptyMsg)).toBeInTheDocument();
  });

  it('does not show emptyMessage when properties exist', () => {
    render(
      <PropertyGrid
        properties={sampleProperties}
        emptyMessage="No properties found."
      />
    );
    expect(screen.queryByTestId('property-grid-empty')).not.toBeInTheDocument();
  });

  it('renders the correct number of property cards', () => {
    render(
      <PropertyGrid
        properties={sampleProperties}
        emptyMessage="No properties found."
      />
    );
    expect(screen.getByTestId('property-card-1')).toBeInTheDocument();
    expect(screen.getByTestId('property-card-2')).toBeInTheDocument();
    expect(screen.getByTestId('property-card-3')).toBeInTheDocument();
  });

  it('renders the grid container with correct test id when properties exist', () => {
    render(
      <PropertyGrid
        properties={sampleProperties}
        emptyMessage="No properties found."
      />
    );
    expect(screen.getByTestId('property-grid-list')).toBeInTheDocument();
  });

  it('calls onPropertyClick when a property card is clicked', async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();

    render(
      <PropertyGrid
        properties={sampleProperties}
        emptyMessage="No properties found."
        onPropertyClick={handleClick}
      />
    );

    await user.click(screen.getByTestId('property-card-2'));
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith(
      expect.objectContaining({ id: '2', title: 'Home Two' })
    );
  });

  it('does not crash when onPropertyClick is not provided', async () => {
    const user = userEvent.setup();

    render(
      <PropertyGrid
        properties={sampleProperties}
        emptyMessage="No properties found."
      />
    );

    // Should not throw
    await user.click(screen.getByTestId('property-card-1'));
  });

  it('passes the first image from images array to PropertyCard', () => {
    const property = createMockProperty({
      id: 'img-test',
      images: [
        'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',
      ],
    });

    render(
      <PropertyGrid
        properties={[property]}
        emptyMessage="No properties found."
      />
    );

    expect(screen.getByTestId('property-card-img-test')).toBeInTheDocument();
  });

  it('handles a property with an empty images array gracefully', () => {
    const property = createMockProperty({ id: 'no-img', images: [] });

    render(
      <PropertyGrid
        properties={[property]}
        emptyMessage="No properties found."
      />
    );

    expect(screen.getByTestId('property-card-no-img')).toBeInTheDocument();
  });
});
