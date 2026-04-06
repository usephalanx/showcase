/**
 * Mock neighborhood data for development and testing.
 *
 * Provides a static array of Neighborhood objects and a helper
 * function to retrieve a neighborhood by slug.
 */

import type { Neighborhood } from "../types/models";

/** Static list of mock neighborhoods. */
export const MOCK_NEIGHBORHOODS: Neighborhood[] = [
  {
    id: "neighborhood-1",
    name: "Downtown Heights",
    slug: "downtown-heights",
    city: "Metropolis",
    state: "CA",
    description:
      "A vibrant urban core with walkable streets, world-class dining, and a thriving arts scene. Downtown Heights offers the best of city living with modern high-rises and converted lofts.",
    image:
      "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop",
    averagePrice: 750000,
    walkScore: 95,
    transitScore: 90,
    highlights: [
      "Walk to restaurants and shops",
      "Excellent public transit",
      "Vibrant nightlife",
      "Farmers market every Saturday",
    ],
    featuredProperties: ["prop-1", "prop-2"],
  },
  {
    id: "neighborhood-2",
    name: "Oakwood Estates",
    slug: "oakwood-estates",
    city: "Metropolis",
    state: "CA",
    description:
      "Tree-lined streets and spacious lots define this family-friendly suburb. Oakwood Estates is known for its top-rated schools, community parks, and friendly neighbors.",
    image:
      "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800&h=600&fit=crop",
    averagePrice: 950000,
    walkScore: 65,
    transitScore: 45,
    highlights: [
      "Top-rated school district",
      "Community pool and playground",
      "Low crime rate",
      "Annual block party",
    ],
    featuredProperties: ["prop-3", "prop-4"],
  },
  {
    id: "neighborhood-3",
    name: "Harbor View",
    slug: "harbor-view",
    city: "Metropolis",
    state: "CA",
    description:
      "Perched along the waterfront, Harbor View combines stunning ocean vistas with a laid-back coastal lifestyle. Enjoy morning jogs along the boardwalk and sunset dining at harborside bistros.",
    image:
      "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&h=600&fit=crop",
    averagePrice: 1200000,
    walkScore: 78,
    transitScore: 55,
    highlights: [
      "Ocean views",
      "Boardwalk and marina",
      "Fresh seafood restaurants",
      "Weekend sailing regattas",
    ],
    featuredProperties: ["prop-5"],
  },
  {
    id: "neighborhood-4",
    name: "Maplewood Commons",
    slug: "maplewood-commons",
    city: "Metropolis",
    state: "CA",
    description:
      "An up-and-coming neighborhood blending historic charm with modern renovations. Maplewood Commons features artisan coffee shops, indie bookstores, and a growing tech-startup presence.",
    image:
      "https://images.unsplash.com/photo-1460317442991-0ec209397118?w=800&h=600&fit=crop",
    averagePrice: 620000,
    walkScore: 88,
    transitScore: 72,
    highlights: [
      "Trendy cafes and boutiques",
      "Historic architecture",
      "Growing tech hub",
      "Dog-friendly parks",
    ],
    featuredProperties: ["prop-6"],
  },
];

/**
 * Retrieve a single neighborhood by its URL-friendly slug.
 *
 * @param slug - The neighborhood slug to look up.
 * @returns The matching Neighborhood object, or undefined if not found.
 */
export function getNeighborhoodBySlug(
  slug: string,
): Neighborhood | undefined {
  return MOCK_NEIGHBORHOODS.find((n) => n.slug === slug);
}
