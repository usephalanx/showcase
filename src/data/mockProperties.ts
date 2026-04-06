import { Property, PropertyStatus } from '../types/models';

export const MOCK_PROPERTIES: Property[] = [
  {
    id: '1',
    title: 'Modern Lakefront Villa',
    slug: 'modern-lakefront-villa',
    price: 1250000,
    address: '123 Lakeview Dr',
    city: 'Austin',
    state: 'TX',
    zipCode: '73301',
    propertyType: 'house',
    bedrooms: 4,
    bathrooms: 3,
    squareFeet: 3200,
    lotSize: '0.5 acres',
    yearBuilt: 2021,
    description: 'Stunning modern villa with panoramic lake views, open floor plan, and luxury finishes throughout.',
    features: ['Pool', 'Lake View', 'Smart Home', 'Wine Cellar'],
    images: [
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop'
    ],
    agent: '1',
    neighborhood: '1',
    listingDate: '2024-01-15',
    status: 'for-sale'
  },
  {
    id: '2',
    title: 'Downtown Luxury Condo',
    slug: 'downtown-luxury-condo',
    price: 675000,
    address: '456 Main St #12A',
    city: 'Denver',
    state: 'CO',
    zipCode: '80202',
    propertyType: 'condo',
    bedrooms: 2,
    bathrooms: 2,
    squareFeet: 1450,
    lotSize: 'N/A',
    yearBuilt: 2019,
    description: 'Elegant downtown condo with floor-to-ceiling windows and skyline views.',
    features: ['Doorman', 'Gym', 'Rooftop Terrace', 'Parking'],
    images: [
      'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop'
    ],
    agent: '2',
    neighborhood: '2',
    listingDate: '2024-02-01',
    status: 'for-sale'
  },
  {
    id: '3',
    title: 'Charming Colonial Townhouse',
    slug: 'charming-colonial-townhouse',
    price: 525000,
    address: '789 Oak Ave',
    city: 'Portland',
    state: 'OR',
    zipCode: '97201',
    propertyType: 'townhouse',
    bedrooms: 3,
    bathrooms: 2,
    squareFeet: 2100,
    lotSize: '0.15 acres',
    yearBuilt: 2005,
    description: 'Beautiful colonial-style townhouse in a tree-lined neighborhood with updated kitchen and hardwood floors.',
    features: ['Hardwood Floors', 'Fireplace', 'Garden', 'Garage'],
    images: [
      'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop'
    ],
    agent: '3',
    neighborhood: '3',
    listingDate: '2024-01-20',
    status: 'for-sale'
  },
  {
    id: '4',
    title: 'Hillside Contemporary Estate',
    slug: 'hillside-contemporary-estate',
    price: 2100000,
    address: '321 Summit Rd',
    city: 'Austin',
    state: 'TX',
    zipCode: '73301',
    propertyType: 'house',
    bedrooms: 5,
    bathrooms: 4,
    squareFeet: 4800,
    lotSize: '1.2 acres',
    yearBuilt: 2022,
    description: 'Architectural masterpiece perched on a hillside with sweeping views and resort-style amenities.',
    features: ['Infinity Pool', 'Home Theater', 'Elevator', 'Solar Panels'],
    images: [
      'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop'
    ],
    agent: '1',
    neighborhood: '1',
    listingDate: '2024-02-10',
    status: 'for-sale'
  },
  {
    id: '5',
    title: 'Cozy Studio Apartment',
    slug: 'cozy-studio-apartment',
    price: 285000,
    address: '55 River Walk Blvd #3B',
    city: 'Denver',
    state: 'CO',
    zipCode: '80202',
    propertyType: 'apartment',
    bedrooms: 1,
    bathrooms: 1,
    squareFeet: 650,
    lotSize: 'N/A',
    yearBuilt: 2018,
    description: 'Efficient and stylish studio apartment in the heart of the riverwalk district.',
    features: ['In-unit Laundry', 'Balcony', 'Pet Friendly'],
    images: [
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop'
    ],
    agent: '4',
    neighborhood: '2',
    listingDate: '2024-03-01',
    status: 'pending'
  },
  {
    id: '6',
    title: 'Rustic Craftsman Bungalow',
    slug: 'rustic-craftsman-bungalow',
    price: 450000,
    address: '900 Elm St',
    city: 'Portland',
    state: 'OR',
    zipCode: '97201',
    propertyType: 'house',
    bedrooms: 3,
    bathrooms: 2,
    squareFeet: 1800,
    lotSize: '0.25 acres',
    yearBuilt: 1948,
    description: 'Lovingly restored craftsman bungalow with original details and modern updates.',
    features: ['Original Woodwork', 'Updated Kitchen', 'Wrap Porch', 'Detached Garage'],
    images: [
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop'
    ],
    agent: '3',
    neighborhood: '4',
    listingDate: '2024-02-20',
    status: 'sold'
  }
];

export function getPropertyBySlug(slug: string): Property | undefined {
  return MOCK_PROPERTIES.find((p) => p.slug === slug);
}

export function getPropertiesByStatus(status: PropertyStatus): Property[] {
  return MOCK_PROPERTIES.filter((p) => p.status === status);
}

export function getFeaturedProperties(): Property[] {
  return MOCK_PROPERTIES.slice(0, 3);
}
