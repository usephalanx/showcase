/**
 * Mock neighborhood data for development.
 *
 * Provides a static array of neighborhoods and a lookup helper.
 */

import type { Neighborhood } from "../types/models";

/** Sample neighborhoods. */
export const MOCK_NEIGHBORHOODS: Neighborhood[] = [
  {
    id: "neighborhood-1",
    name: "Lakewood Hills",
    slug: "lakewood-hills",
    city: "Austin",
    state: "TX",
    description:
      "An exclusive lakeside community known for its luxury estates, scenic trails, and top-rated schools. Residents enjoy private lake access, boat docks, and a peaceful retreat minutes from downtown.",
    image:
      "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop",
    averagePrice: 1_100_000,
    walkScore: 45,
    transitScore: 30,
    highlights: [
      "Private Lake Access",
      "Top-Rated Schools",
      "Scenic Hiking Trails",
      "Gated Communities",
    ],
    featuredProperties: ["prop-1"],
  },
  {
    id: "neighborhood-2",
    name: "Downtown",
    slug: "downtown",
    city: "Austin",
    state: "TX",
    description:
      "The vibrant urban core with world-class dining, live music venues, and stunning skyline views. High-rise condos and lofts put you steps away from everything the city has to offer.",
    image:
      "https://images.unsplash.com/photo-1444723121867-7a241cacace9?w=800&h=600&fit=crop",
    averagePrice: 750_000,
    walkScore: 95,
    transitScore: 85,
    highlights: [
      "Live Music Capital",
      "Walkable Everywhere",
      "Rooftop Bars & Restaurants",
      "Lady Bird Lake Access",
    ],
    featuredProperties: ["prop-2"],
  },
  {
    id: "neighborhood-3",
    name: "South Congress",
    slug: "south-congress",
    city: "Austin",
    state: "TX",
    description:
      "Eclectic and colorful, SoCo is famous for its boutique shopping, food trucks, and artistic vibe. Charming bungalows and renovated homes line the tree-shaded streets just south of the river.",
    image:
      "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=800&h=600&fit=crop",
    averagePrice: 550_000,
    walkScore: 82,
    transitScore: 60,
    highlights: [
      "Boutique Shopping",
      "Food Truck Paradise",
      "Art Galleries",
      "Historic Architecture",
    ],
    featuredProperties: ["prop-3"],
  },
  {
    id: "neighborhood-4",
    name: "Westlake Hills",
    slug: "westlake-hills",
    city: "Austin",
    state: "TX",
    description:
      "A prestigious enclave in the Texas Hill Country offering panoramic views, sprawling estates, and acclaimed Eanes ISD schools. The area blends natural beauty with sophisticated luxury living.",
    image:
      "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&h=600&fit=crop",
    averagePrice: 1_500_000,
    walkScore: 25,
    transitScore: 15,
    highlights: [
      "Hill Country Views",
      "Eanes ISD Schools",
      "Nature Preserves",
      "Luxury Estates",
    ],
    featuredProperties: ["prop-4"],
  },
];

/**
 * Look up a single neighborhood by its URL slug.
 *
 * @param slug - The URL-friendly slug to search for.
 * @returns The matching Neighborhood, or undefined if not found.
 */
export function getNeighborhoodBySlug(slug: string): Neighborhood | undefined {
  return MOCK_NEIGHBORHOODS.find((n) => n.slug === slug);
}
