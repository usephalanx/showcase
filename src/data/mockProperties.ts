/**
 * Mock property data with Unsplash image URLs for development.
 */

import type { Property, PropertyStatus } from '../types/models';
import { MOCK_AGENTS } from './mockAgents';
import { MOCK_NEIGHBORHOODS } from './mockNeighborhoods';

/** Sample properties used throughout the application during development. */
export const MOCK_PROPERTIES: Property[] = [
  {
    id: 'prop-1',
    title: 'Modern Farmhouse with Open Floor Plan',
    slug: 'modern-farmhouse-open-floor-plan',
    price: 625000,
    address: '1234 Maple Grove Lane',
    city: 'Austin',
    state: 'TX',
    zipCode: '78701',
    propertyType: 'house',
    bedrooms: 4,
    bathrooms: 3,
    squareFeet: 2850,
    lotSize: 0.35,
    yearBuilt: 2021,
    description:
      'This stunning modern farmhouse features an open-concept living area with soaring ceilings, a gourmet kitchen with quartz countertops, and a spacious primary suite. The backyard oasis includes a covered patio and mature landscaping.',
    features: [
      'Open floor plan',
      'Quartz countertops',
      'Hardwood floors',
      'Smart home system',
      'Covered patio',
      'Two-car garage',
    ],
    images: [
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
    ],
    agent: MOCK_AGENTS[0],
    neighborhood: MOCK_NEIGHBORHOODS[0],
    listingDate: '2024-01-15',
    status: 'for-sale',
  },
  {
    id: 'prop-2',
    title: 'Charming Craftsman Bungalow',
    slug: 'charming-craftsman-bungalow',
    price: 475000,
    address: '567 Oak Street',
    city: 'Austin',
    state: 'TX',
    zipCode: '78702',
    propertyType: 'house',
    bedrooms: 3,
    bathrooms: 2,
    squareFeet: 1950,
    lotSize: 0.25,
    yearBuilt: 1948,
    description:
      'A beautifully restored Craftsman bungalow with original hardwood floors, built-in bookshelves, and a charming front porch. Updated kitchen and bathrooms blend modern convenience with period character.',
    features: [
      'Original hardwood floors',
      'Built-in bookshelves',
      'Updated kitchen',
      'Front porch',
      'Fenced backyard',
      'Detached garage',
    ],
    images: [
      'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
    ],
    agent: MOCK_AGENTS[1],
    neighborhood: MOCK_NEIGHBORHOODS[0],
    listingDate: '2024-02-01',
    status: 'for-sale',
  },
  {
    id: 'prop-3',
    title: 'Luxury Waterfront Penthouse',
    slug: 'luxury-waterfront-penthouse',
    price: 1250000,
    address: '200 Riverside Drive, PH-1',
    city: 'Austin',
    state: 'TX',
    zipCode: '78703',
    propertyType: 'condo',
    bedrooms: 3,
    bathrooms: 3.5,
    squareFeet: 3200,
    lotSize: 0,
    yearBuilt: 2023,
    description:
      'An exceptional penthouse offering panoramic river views from floor-to-ceiling windows. Features include a private elevator, chef\'s kitchen with top-of-the-line appliances, and a wraparound terrace perfect for entertaining.',
    features: [
      'Panoramic river views',
      'Private elevator',
      'Chef\'s kitchen',
      'Wraparound terrace',
      'Wine cellar',
      'Concierge service',
    ],
    images: [
      'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
    ],
    agent: MOCK_AGENTS[3],
    neighborhood: MOCK_NEIGHBORHOODS[1],
    listingDate: '2024-01-20',
    status: 'for-sale',
  },
  {
    id: 'prop-4',
    title: 'Contemporary Riverside Townhome',
    slug: 'contemporary-riverside-townhome',
    price: 725000,
    address: '88 River Walk Court',
    city: 'Austin',
    state: 'TX',
    zipCode: '78703',
    propertyType: 'townhouse',
    bedrooms: 3,
    bathrooms: 2.5,
    squareFeet: 2400,
    lotSize: 0.1,
    yearBuilt: 2022,
    description:
      'A sleek contemporary townhome with an open layout, rooftop deck, and direct access to the river walk trail. High-end finishes throughout, including waterfall island, spa-like primary bath, and custom closets.',
    features: [
      'Rooftop deck',
      'River walk access',
      'Waterfall island',
      'Spa-like primary bath',
      'Custom closets',
      'EV charging station',
    ],
    images: [
      'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
    ],
    agent: MOCK_AGENTS[2],
    neighborhood: MOCK_NEIGHBORHOODS[1],
    listingDate: '2024-02-10',
    status: 'pending',
  },
  {
    id: 'prop-5',
    title: 'Mountain View Estate',
    slug: 'mountain-view-estate',
    price: 1850000,
    address: '9500 Summit Ridge Road',
    city: 'Denver',
    state: 'CO',
    zipCode: '80202',
    propertyType: 'house',
    bedrooms: 5,
    bathrooms: 4.5,
    squareFeet: 5200,
    lotSize: 1.2,
    yearBuilt: 2020,
    description:
      'A breathtaking mountain estate with unobstructed views of the Rockies. This architectural masterpiece features walls of glass, a resort-style pool, home theater, and a six-car garage.',
    features: [
      'Mountain views',
      'Resort-style pool',
      'Home theater',
      'Wine cellar',
      'Six-car garage',
      'Home gym',
    ],
    images: [
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop',
    ],
    agent: MOCK_AGENTS[0],
    neighborhood: MOCK_NEIGHBORHOODS[2],
    listingDate: '2024-01-05',
    status: 'for-sale',
  },
  {
    id: 'prop-6',
    title: 'Harbor View Apartment',
    slug: 'harbor-view-apartment',
    price: 550000,
    address: '350 Harbor Boulevard, Unit 12C',
    city: 'Seattle',
    state: 'WA',
    zipCode: '98101',
    propertyType: 'apartment',
    bedrooms: 2,
    bathrooms: 2,
    squareFeet: 1400,
    lotSize: 0,
    yearBuilt: 2019,
    description:
      'A bright and airy apartment with sweeping views of Puget Sound. Features include an open kitchen with breakfast bar, in-unit laundry, and access to building amenities including a gym, pool, and rooftop lounge.',
    features: [
      'Sound views',
      'In-unit laundry',
      'Building gym',
      'Rooftop lounge',
      'Concierge',
      'Pet-friendly',
    ],
    images: [
      'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
    ],
    agent: MOCK_AGENTS[1],
    neighborhood: MOCK_NEIGHBORHOODS[3],
    listingDate: '2024-02-20',
    status: 'sold',
  },
];

/**
 * Find a property by its URL-friendly slug.
 *
 * @param slug - The property's slug string.
 * @returns The matching Property or undefined if not found.
 */
export function getPropertyBySlug(slug: string): Property | undefined {
  return MOCK_PROPERTIES.find((p) => p.slug === slug);
}

/**
 * Filter properties by their listing status.
 *
 * @param status - The status to filter by.
 * @returns An array of properties matching the given status.
 */
export function getPropertiesByStatus(status: PropertyStatus): Property[] {
  return MOCK_PROPERTIES.filter((p) => p.status === status);
}

/**
 * Return the first 3 properties as featured listings.
 *
 * @returns An array of up to 3 featured properties.
 */
export function getFeaturedProperties(): Property[] {
  return MOCK_PROPERTIES.slice(0, 3);
}
