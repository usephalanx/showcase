/**
 * Mock property listing data for development and testing.
 *
 * Contains 12+ realistic property entries with real Unsplash photo IDs
 * for exterior shots, interior photography, and lifestyle images.
 */

import type { Property, PropertyStatus } from '../types/models';

export const MOCK_PROPERTIES: Property[] = [
  {
    id: 'prop-001',
    title: 'Modern Lakefront Estate',
    slug: 'modern-lakefront-estate',
    price: 1250000,
    address: '142 Lakeshore Drive',
    city: 'Austin',
    state: 'TX',
    zipCode: '78701',
    propertyType: 'house',
    bedrooms: 5,
    bathrooms: 4.5,
    squareFeet: 4200,
    lotSize: 0.85,
    yearBuilt: 2021,
    description:
      'Stunning contemporary estate on the shores of Lake Austin. Floor-to-ceiling windows flood every room with natural light while providing panoramic water views. The open-concept living area features a chef's kitchen with Thermador appliances, waterfall quartz island, and custom cabinetry. A private dock and infinity pool complete this luxury retreat.',
    features: [
      'Private boat dock',
      'Infinity pool',
      'Home theater',
      'Wine cellar',
      'Smart home system',
      'Three-car garage',
    ],
    images: [
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop',
    ],
    featured: true,
    agentId: 'agent-001',
    neighborhoodId: 'hood-001',
    listingDate: '2024-09-15',
    status: 'for-sale',
  },
  {
    id: 'prop-002',
    title: 'Downtown Luxury Condo',
    slug: 'downtown-luxury-condo',
    price: 685000,
    address: '900 Congress Ave #2204',
    city: 'Austin',
    state: 'TX',
    zipCode: '78701',
    propertyType: 'condo',
    bedrooms: 2,
    bathrooms: 2,
    squareFeet: 1450,
    yearBuilt: 2019,
    description:
      'Sleek high-rise living in the heart of downtown Austin. This 22nd-floor unit boasts sweeping skyline views, designer finishes, and resort-style amenities including a rooftop pool, concierge service, and state-of-the-art fitness center. Walk to Rainey Street, Lady Bird Lake, and world-class dining.',
    features: [
      'Rooftop pool',
      'Concierge service',
      'Floor-to-ceiling windows',
      'EV charging',
      'Pet-friendly',
    ],
    images: [
      'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
    ],
    featured: true,
    agentId: 'agent-002',
    neighborhoodId: 'hood-002',
    listingDate: '2024-10-01',
    status: 'for-sale',
  },
  {
    id: 'prop-003',
    title: 'Charming Craftsman Bungalow',
    slug: 'charming-craftsman-bungalow',
    price: 475000,
    address: '3218 Oak Hollow Lane',
    city: 'Austin',
    state: 'TX',
    zipCode: '78704',
    propertyType: 'house',
    bedrooms: 3,
    bathrooms: 2,
    squareFeet: 1850,
    lotSize: 0.28,
    yearBuilt: 1948,
    description:
      'Lovingly restored 1940s Craftsman bungalow in the heart of South Austin. Original hardwood floors, built-in bookshelves, and a wraparound porch give this home timeless character. Updated kitchen and bathrooms blend period charm with modern convenience. Mature pecan trees shade the generous backyard.',
    features: [
      'Original hardwood floors',
      'Wraparound porch',
      'Updated kitchen',
      'Mature trees',
      'Detached studio',
    ],
    images: [
      'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
    ],
    featured: true,
    agentId: 'agent-003',
    neighborhoodId: 'hood-003',
    listingDate: '2024-08-20',
    status: 'for-sale',
  },
  {
    id: 'prop-004',
    title: 'Hill Country Contemporary',
    slug: 'hill-country-contemporary',
    price: 925000,
    address: '7801 Scenic Brook Ct',
    city: 'Austin',
    state: 'TX',
    zipCode: '78735',
    propertyType: 'house',
    bedrooms: 4,
    bathrooms: 3.5,
    squareFeet: 3400,
    lotSize: 1.2,
    yearBuilt: 2020,
    description:
      'Perched on a hilltop with breathtaking views of the Texas Hill Country, this contemporary masterpiece seamlessly blends indoor and outdoor living. Walls of glass open to expansive limestone terraces, a resort-style pool, and native landscaping. Premium finishes throughout include white oak floors, Calacatta marble, and custom steel doors.',
    features: [
      'Hill Country views',
      'Resort-style pool',
      'Outdoor kitchen',
      'White oak floors',
      'Three-car garage',
      'Home office',
    ],
    images: [
      'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
    ],
    featured: false,
    agentId: 'agent-001',
    neighborhoodId: 'hood-004',
    listingDate: '2024-10-10',
    status: 'for-sale',
  },
  {
    id: 'prop-005',
    title: 'East Side Townhome',
    slug: 'east-side-townhome',
    price: 520000,
    address: '1105 Chicon St Unit B',
    city: 'Austin',
    state: 'TX',
    zipCode: '78702',
    propertyType: 'townhouse',
    bedrooms: 3,
    bathrooms: 2.5,
    squareFeet: 1900,
    yearBuilt: 2022,
    description:
      'Brand-new construction townhome in the vibrant East Austin corridor. Clean Scandinavian-inspired design features open-plan living, a gourmet kitchen with waterfall island, and a private rooftop deck with skyline views. Steps from acclaimed restaurants, galleries, and the hike-and-bike trail.',
    features: [
      'Rooftop deck',
      'Skyline views',
      'Gourmet kitchen',
      'Two-car garage',
      'Energy efficient',
    ],
    images: [
      'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
    ],
    featured: false,
    agentId: 'agent-002',
    neighborhoodId: 'hood-005',
    listingDate: '2024-09-28',
    status: 'for-sale',
  },
  {
    id: 'prop-006',
    title: 'Riverside Park Apartment',
    slug: 'riverside-park-apartment',
    price: 325000,
    address: '2200 S Lakeshore Blvd #310',
    city: 'Austin',
    state: 'TX',
    zipCode: '78741',
    propertyType: 'apartment',
    bedrooms: 1,
    bathrooms: 1,
    squareFeet: 850,
    yearBuilt: 2017,
    description:
      'Stylish one-bedroom apartment overlooking the Colorado River. Modern finishes include quartz countertops, stainless appliances, and luxury vinyl plank flooring. Community amenities feature a lap pool, dog park, and coworking lounge. Ideal for professionals seeking low-maintenance urban living.',
    features: [
      'River views',
      'Lap pool',
      'Dog park',
      'Coworking lounge',
      'Bike storage',
    ],
    images: [
      'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
    ],
    featured: false,
    agentId: 'agent-003',
    neighborhoodId: 'hood-006',
    listingDate: '2024-10-05',
    status: 'for-sale',
  },
  {
    id: 'prop-007',
    title: 'Westlake Family Retreat',
    slug: 'westlake-family-retreat',
    price: 1475000,
    address: '4500 Westlake Dr',
    city: 'Austin',
    state: 'TX',
    zipCode: '78746',
    propertyType: 'house',
    bedrooms: 5,
    bathrooms: 4,
    squareFeet: 4600,
    lotSize: 0.95,
    yearBuilt: 2018,
    description:
      'Elegant family home in the prestigious Westlake neighborhood with access to top-rated Eanes ISD schools. A grand foyer opens to soaring ceilings and a wall of windows framing lush greenery. Chef's kitchen, media room, exercise studio, and a resort-caliber backyard with pool, spa, and outdoor fireplace.',
    features: [
      'Pool and spa',
      'Outdoor fireplace',
      'Media room',
      'Exercise studio',
      'Eanes ISD',
      'Four-car garage',
    ],
    images: [
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',
    ],
    featured: false,
    agentId: 'agent-001',
    neighborhoodId: 'hood-004',
    listingDate: '2024-07-12',
    status: 'pending',
  },
  {
    id: 'prop-008',
    title: 'Mueller Mid-Century Modern',
    slug: 'mueller-mid-century-modern',
    price: 610000,
    address: '1920 Aldrich St #12',
    city: 'Austin',
    state: 'TX',
    zipCode: '78723',
    propertyType: 'townhouse',
    bedrooms: 3,
    bathrooms: 2.5,
    squareFeet: 2050,
    yearBuilt: 2016,
    description:
      'Award-winning mid-century-inspired townhome in the master-planned Mueller community. Clean lines, abundant natural light, and an open floor plan define this thoughtfully designed residence. Walk to Thinkery children's museum, the farmers' market, and acres of parkland.',
    features: [
      'Mid-century design',
      'Open floor plan',
      'Community parks',
      'Farmers' market nearby',
      'Solar panels',
    ],
    images: [
      'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop',
    ],
    featured: false,
    agentId: 'agent-002',
    neighborhoodId: 'hood-005',
    listingDate: '2024-06-30',
    status: 'sold',
  },
  {
    id: 'prop-009',
    title: 'SoCo Artistic Retreat',
    slug: 'soco-artistic-retreat',
    price: 555000,
    address: '2406 S 1st St',
    city: 'Austin',
    state: 'TX',
    zipCode: '78704',
    propertyType: 'house',
    bedrooms: 2,
    bathrooms: 2,
    squareFeet: 1400,
    lotSize: 0.18,
    yearBuilt: 1955,
    description:
      'Eclectic cottage on iconic South Congress Avenue. Fully renovated with an artist's eye—polished concrete floors, exposed beam ceilings, and a chef's kitchen with butcher block counters. The private backyard oasis features string lights, a fire pit, and native plantings. Walk to SoCo shops, food trucks, and live music.',
    features: [
      'Polished concrete floors',
      'Exposed beams',
      'Backyard oasis',
      'Walk to SoCo',
      'Renovated kitchen',
    ],
    images: [
      'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop',
    ],
    featured: false,
    agentId: 'agent-003',
    neighborhoodId: 'hood-003',
    listingDate: '2024-09-01',
    status: 'for-sale',
  },
  {
    id: 'prop-010',
    title: 'Domain Luxury Penthouse',
    slug: 'domain-luxury-penthouse',
    price: 890000,
    address: '11511 Rock Rose Ave PH-1',
    city: 'Austin',
    state: 'TX',
    zipCode: '78758',
    propertyType: 'condo',
    bedrooms: 3,
    bathrooms: 3,
    squareFeet: 2400,
    yearBuilt: 2023,
    description:
      'Top-floor penthouse in the Domain's newest luxury tower. Wraparound terrace offers 270-degree views of the Austin skyline. Italian porcelain tile, German-engineered kitchen, spa-like primary bath, and a private elevator entry. Steps from upscale shopping, dining, and entertainment.',
    features: [
      'Private elevator',
      'Wraparound terrace',
      'Italian porcelain tile',
      'Skyline views',
      'Valet parking',
      'Spa-like primary bath',
    ],
    images: [
      'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
    ],
    featured: false,
    agentId: 'agent-001',
    neighborhoodId: 'hood-002',
    listingDate: '2024-10-15',
    status: 'for-sale',
  },
  {
    id: 'prop-011',
    title: 'Barton Creek Colonial',
    slug: 'barton-creek-colonial',
    price: 1150000,
    address: '8200 Barton Club Dr',
    city: 'Austin',
    state: 'TX',
    zipCode: '78735',
    propertyType: 'house',
    bedrooms: 4,
    bathrooms: 3.5,
    squareFeet: 3800,
    lotSize: 0.65,
    yearBuilt: 2005,
    description:
      'Stately colonial on the Barton Creek greenbelt with mature oak canopy and seasonal creek views. Formal living and dining rooms, a large family room with stone fireplace, and an updated gourmet kitchen. The primary suite includes a sitting area, dual walk-in closets, and a spa bath. Community golf course and tennis courts.',
    features: [
      'Greenbelt lot',
      'Stone fireplace',
      'Gourmet kitchen',
      'Community golf course',
      'Tennis courts',
      'Three-car garage',
    ],
    images: [
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
    ],
    featured: false,
    agentId: 'agent-002',
    neighborhoodId: 'hood-004',
    listingDate: '2024-08-05',
    status: 'pending',
  },
  {
    id: 'prop-012',
    title: 'Riverside Loft Conversion',
    slug: 'riverside-loft-conversion',
    price: 415000,
    address: '1800 E Riverside Dr #405',
    city: 'Austin',
    state: 'TX',
    zipCode: '78741',
    propertyType: 'apartment',
    bedrooms: 2,
    bathrooms: 2,
    squareFeet: 1200,
    yearBuilt: 2015,
    description:
      'Industrial-chic loft in a converted warehouse along the Riverside corridor. Soaring 14-foot ceilings, exposed brick walls, and oversized factory windows create a dramatic living space. Updated with contemporary fixtures, a sleek kitchen, and in-unit laundry. Minutes from downtown via the Metro Rail.',
    features: [
      '14-foot ceilings',
      'Exposed brick',
      'Factory windows',
      'In-unit laundry',
      'Metro Rail access',
    ],
    images: [
      'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
    ],
    featured: false,
    agentId: 'agent-003',
    neighborhoodId: 'hood-006',
    listingDate: '2024-10-18',
    status: 'for-sale',
  },
  {
    id: 'prop-013',
    title: 'Travis Heights Victorian',
    slug: 'travis-heights-victorian',
    price: 795000,
    address: '1100 Travis Heights Blvd',
    city: 'Austin',
    state: 'TX',
    zipCode: '78704',
    propertyType: 'house',
    bedrooms: 4,
    bathrooms: 3,
    squareFeet: 2600,
    lotSize: 0.32,
    yearBuilt: 1925,
    description:
      'Beautifully preserved Victorian in the coveted Travis Heights neighborhood. Period details—stained glass transoms, crown molding, clawfoot tubs—coexist with a modern addition featuring a gourmet kitchen and glass-walled family room. Terraced garden with city-skyline views.',
    features: [
      'Stained glass transoms',
      'Clawfoot tubs',
      'Terraced garden',
      'Skyline views',
      'Modern addition',
    ],
    images: [
      'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
    ],
    featured: false,
    agentId: 'agent-001',
    neighborhoodId: 'hood-003',
    listingDate: '2024-07-22',
    status: 'sold',
  },
];

/**
 * Look up a single property by its URL-friendly slug.
 *
 * @param slug - The slug to search for.
 * @returns The matching Property or undefined.
 */
export function getPropertyBySlug(slug: string): Property | undefined {
  return MOCK_PROPERTIES.find((p) => p.slug === slug);
}

/**
 * Filter properties by their sales status.
 *
 * @param status - The PropertyStatus to filter on.
 * @returns An array of matching properties.
 */
export function getPropertiesByStatus(status: PropertyStatus): Property[] {
  return MOCK_PROPERTIES.filter((p) => p.status === status);
}

/**
 * Return the set of properties marked as featured.
 *
 * @returns The first three featured properties.
 */
export function getFeaturedProperties(): Property[] {
  return MOCK_PROPERTIES.filter((p) => p.featured).slice(0, 3);
}

/**
 * Look up a single property by its unique ID.
 *
 * @param id - The property ID to search for.
 * @returns The matching Property or undefined.
 */
export function getPropertyById(id: string): Property | undefined {
  return MOCK_PROPERTIES.find((p) => p.id === id);
}

/**
 * Return all properties associated with a given neighborhood.
 *
 * @param neighborhoodId - The neighborhood ID to filter on.
 * @returns An array of matching properties.
 */
export function getPropertiesByNeighborhood(neighborhoodId: string): Property[] {
  return MOCK_PROPERTIES.filter((p) => p.neighborhoodId === neighborhoodId);
}

/**
 * Return all properties listed by a given agent.
 *
 * @param agentId - The agent ID to filter on.
 * @returns An array of matching properties.
 */
export function getPropertiesByAgent(agentId: string): Property[] {
  return MOCK_PROPERTIES.filter((p) => p.agentId === agentId);
}
