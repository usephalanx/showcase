/**
 * Mock neighborhood data with Unsplash cityscape/neighborhood URLs for development.
 */

import type { Neighborhood } from '../types/models';

/** Sample neighborhoods used throughout the application during development. */
export const MOCK_NEIGHBORHOODS: Neighborhood[] = [
  {
    id: 'neighborhood-1',
    name: 'Maple Heights',
    slug: 'maple-heights',
    city: 'Austin',
    state: 'TX',
    description: 'A tree-lined neighborhood known for its charming bungalows, vibrant local shops, and excellent school district. Maple Heights offers a perfect blend of suburban tranquility and urban convenience.',
    image: 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop',
    averagePrice: 585000,
    walkScore: 82,
    transitScore: 68,
    highlights: ['Top-rated schools', 'Farmers market', 'Dog parks', 'Bike trails'],
    featuredProperties: ['prop-1', 'prop-2'],
  },
  {
    id: 'neighborhood-2',
    name: 'Riverside District',
    slug: 'riverside-district',
    city: 'Austin',
    state: 'TX',
    description: 'Situated along the banks of the Colorado River, the Riverside District features stunning waterfront properties, upscale dining, and a thriving arts scene.',
    image: 'https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=800&h=600&fit=crop',
    averagePrice: 875000,
    walkScore: 90,
    transitScore: 78,
    highlights: ['Waterfront views', 'Fine dining', 'Art galleries', 'Marina access'],
    featuredProperties: ['prop-3', 'prop-4'],
  },
  {
    id: 'neighborhood-3',
    name: 'Summit Park',
    slug: 'summit-park',
    city: 'Denver',
    state: 'CO',
    description: 'An upscale community nestled in the foothills with panoramic mountain views, modern architecture, and miles of hiking trails right at your doorstep.',
    image: 'https://images.unsplash.com/photo-1444723121867-7a241cacace9?w=800&h=600&fit=crop',
    averagePrice: 1250000,
    walkScore: 55,
    transitScore: 42,
    highlights: ['Mountain views', 'Hiking trails', 'Gated community', 'Golf course'],
    featuredProperties: ['prop-5'],
  },
  {
    id: 'neighborhood-4',
    name: 'Harbor Point',
    slug: 'harbor-point',
    city: 'Seattle',
    state: 'WA',
    description: 'A vibrant waterfront neighborhood offering stunning Puget Sound views, eclectic restaurants, and a strong sense of community with year-round events.',
    image: 'https://images.unsplash.com/photo-1514565131-fce0801e5785?w=800&h=600&fit=crop',
    averagePrice: 950000,
    walkScore: 88,
    transitScore: 85,
    highlights: ['Sound views', 'Ferry access', 'Seafood restaurants', 'Kayaking'],
    featuredProperties: ['prop-6'],
  },
];

/**
 * Find a neighborhood by its unique identifier.
 *
 * @param id - The neighborhood's unique id string.
 * @returns The matching Neighborhood or undefined if not found.
 */
export function getNeighborhoodById(id: string): Neighborhood | undefined {
  return MOCK_NEIGHBORHOODS.find((n) => n.id === id);
}

/**
 * Find a neighborhood by its URL-friendly slug.
 *
 * @param slug - The neighborhood's slug string.
 * @returns The matching Neighborhood or undefined if not found.
 */
export function getNeighborhoodBySlug(slug: string): Neighborhood | undefined {
  return MOCK_NEIGHBORHOODS.find((n) => n.slug === slug);
}
