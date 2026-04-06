/**
 * Mock neighborhood data for development and testing.
 *
 * Contains 6 Austin-area neighborhoods with real Unsplash photo IDs
 * for cityscape, aerial, and street-level imagery.
 */

import type { Neighborhood } from '../types/models';

export const MOCK_NEIGHBORHOODS: Neighborhood[] = [
  {
    id: 'hood-001',
    name: 'Lake Austin',
    slug: 'lake-austin',
    city: 'Austin',
    state: 'TX',
    description:
      'Nestled along the shores of Lake Austin, this exclusive enclave offers waterfront living at its finest. Residents enjoy private docks, stunning sunsets, and easy access to boating, paddle boarding, and swimming. Despite its serene setting, downtown Austin is only a 20-minute drive away.',
    image:
      'https://images.unsplash.com/photo-1444723121867-7a241cacace9?w=800&h=600&fit=crop',
    averagePrice: 1350000,
    walkScore: 35,
    transitScore: 20,
    highlights: [
      'Waterfront living',
      'Private boat docks',
      'Scenic hill views',
      'Top-rated schools',
      'Low density',
    ],
    featuredPropertyIds: ['prop-001'],
  },
  {
    id: 'hood-002',
    name: 'Downtown Austin',
    slug: 'downtown-austin',
    city: 'Austin',
    state: 'TX',
    description:
      'The beating heart of Austin—a dynamic blend of live music venues, farm-to-table restaurants, tech company headquarters, and luxury high-rises. Downtown living means walking to Lady Bird Lake, Zilker Park, and the famous Sixth Street entertainment district. Perfect for professionals who crave an urban lifestyle.',
    image:
      'https://images.unsplash.com/photo-1531218150217-54595bc2b934?w=800&h=600&fit=crop',
    averagePrice: 725000,
    walkScore: 92,
    transitScore: 78,
    highlights: [
      'Walkable urban core',
      'Live music capital',
      'Lady Bird Lake access',
      'Vibrant nightlife',
      'Tech hub',
    ],
    featuredPropertyIds: ['prop-002', 'prop-010'],
  },
  {
    id: 'hood-003',
    name: 'South Congress (SoCo)',
    slug: 'south-congress',
    city: 'Austin',
    state: 'TX',
    description:
      'South Congress is Austin\'s most iconic street—a colorful stretch of boutiques, food trucks, vintage shops, and mural-covered walls. The surrounding residential streets feature a charming mix of renovated bungalows, mid-century ranches, and new modern builds. SoCo captures the "Keep Austin Weird" spirit better than anywhere else in the city.',
    image:
      'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800&h=600&fit=crop',
    averagePrice: 620000,
    walkScore: 82,
    transitScore: 55,
    highlights: [
      'Iconic shopping street',
      'Food truck culture',
      'Historic bungalows',
      'Art galleries',
      'Close to Zilker Park',
    ],
    featuredPropertyIds: ['prop-003', 'prop-009', 'prop-013'],
  },
  {
    id: 'hood-004',
    name: 'Westlake Hills',
    slug: 'westlake-hills',
    city: 'Austin',
    state: 'TX',
    description:
      'An affluent enclave west of downtown, Westlake Hills is renowned for its top-rated Eanes ISD schools, rolling terrain, and luxurious estates. Residents enjoy proximity to Barton Creek Greenbelt hiking, upscale shopping at the Hill Country Galleria, and quick access to both downtown and the Hill Country wine region.',
    image:
      'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&h=600&fit=crop',
    averagePrice: 1100000,
    walkScore: 28,
    transitScore: 15,
    highlights: [
      'Top-rated Eanes ISD',
      'Barton Creek Greenbelt',
      'Luxury estates',
      'Hill Country views',
      'Country club communities',
    ],
    featuredPropertyIds: ['prop-004', 'prop-007', 'prop-011'],
  },
  {
    id: 'hood-005',
    name: 'East Austin',
    slug: 'east-austin',
    city: 'Austin',
    state: 'TX',
    description:
      'Once the city\'s best-kept secret, East Austin has blossomed into one of the most exciting neighborhoods in the country. A thriving arts scene, James Beard-nominated restaurants, craft breweries, and innovative new construction sit alongside colorful historic homes. The area offers outstanding value with a creative, community-driven vibe.',
    image:
      'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop',
    averagePrice: 540000,
    walkScore: 75,
    transitScore: 50,
    highlights: [
      'Thriving arts scene',
      'Award-winning restaurants',
      'Craft breweries',
      'New construction',
      'Strong appreciation',
    ],
    featuredPropertyIds: ['prop-005', 'prop-008'],
  },
  {
    id: 'hood-006',
    name: 'Riverside',
    slug: 'riverside',
    city: 'Austin',
    state: 'TX',
    description:
      'Riverside is Austin\'s most rapidly transforming corridor. Major mixed-use developments, new transit infrastructure, and proximity to the river make it a magnet for young professionals and investors alike. Affordable price points relative to downtown—just across the bridge—make Riverside one of the best value propositions in central Austin.',
    image:
      'https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=800&h=600&fit=crop',
    averagePrice: 380000,
    walkScore: 68,
    transitScore: 62,
    highlights: [
      'Rapid development',
      'Affordable entry point',
      'River trail access',
      'New transit lines',
      'Close to downtown',
    ],
    featuredPropertyIds: ['prop-006', 'prop-012'],
  },
];

/**
 * Look up a single neighborhood by its URL-friendly slug.
 *
 * @param slug - The slug to search for.
 * @returns The matching Neighborhood or undefined.
 */
export function getNeighborhoodBySlug(slug: string): Neighborhood | undefined {
  return MOCK_NEIGHBORHOODS.find((n) => n.slug === slug);
}

/**
 * Look up a single neighborhood by its unique ID.
 *
 * @param id - The neighborhood ID to search for.
 * @returns The matching Neighborhood or undefined.
 */
export function getNeighborhoodById(id: string): Neighborhood | undefined {
  return MOCK_NEIGHBORHOODS.find((n) => n.id === id);
}
