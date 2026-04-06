/**
 * Mock property listing data for development.
 *
 * Provides a static array of properties and several lookup / filter helpers.
 */

import type { Property, PropertyStatus } from "../types/models";
import { MOCK_AGENTS } from "./mockAgents";

/** Sample property listings. */
export const MOCK_PROPERTIES: Property[] = [
  {
    id: "prop-1",
    title: "Modern Lakefront Estate",
    slug: "modern-lakefront-estate",
    price: 1_250_000,
    address: "742 Lakeview Drive",
    city: "Austin",
    state: "TX",
    zipCode: "78701",
    propertyType: "house",
    bedrooms: 5,
    bathrooms: 4.5,
    squareFeet: 4_200,
    lotSize: 12_000,
    yearBuilt: 2021,
    description:
      "Stunning modern estate overlooking the lake with floor-to-ceiling windows, an open-concept living area, gourmet kitchen with premium appliances, and a resort-style backyard featuring an infinity pool and outdoor kitchen.",
    features: [
      "Infinity Pool",
      "Smart Home System",
      "Wine Cellar",
      "3-Car Garage",
      "Home Theater",
      "Waterfront Access",
    ],
    images: [
      "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop",
    ],
    agent: MOCK_AGENTS[0]!,
    neighborhood: "Lakewood Hills",
    listingDate: "2024-10-15",
    status: "for-sale",
  },
  {
    id: "prop-2",
    title: "Downtown Luxury Penthouse",
    slug: "downtown-luxury-penthouse",
    price: 875_000,
    address: "100 Congress Ave, Unit PH-1",
    city: "Austin",
    state: "TX",
    zipCode: "78702",
    propertyType: "condo",
    bedrooms: 3,
    bathrooms: 2.5,
    squareFeet: 2_800,
    yearBuilt: 2023,
    description:
      "Breathtaking penthouse in the heart of downtown with panoramic skyline views, designer finishes throughout, a private rooftop terrace, and access to world-class building amenities.",
    features: [
      "Rooftop Terrace",
      "Concierge Service",
      "Floor-to-Ceiling Windows",
      "Fitness Center",
      "Valet Parking",
    ],
    images: [
      "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop",
    ],
    agent: MOCK_AGENTS[1]!,
    neighborhood: "Downtown",
    listingDate: "2024-11-01",
    status: "for-sale",
  },
  {
    id: "prop-3",
    title: "Charming Craftsman Bungalow",
    slug: "charming-craftsman-bungalow",
    price: 525_000,
    address: "318 Oak Street",
    city: "Austin",
    state: "TX",
    zipCode: "78704",
    propertyType: "house",
    bedrooms: 3,
    bathrooms: 2,
    squareFeet: 1_850,
    lotSize: 6_500,
    yearBuilt: 1935,
    description:
      "Beautifully restored 1935 Craftsman bungalow with original hardwood floors, built-in bookshelves, updated kitchen and bathrooms, and a lush private garden. Walking distance to vibrant South Congress shops and restaurants.",
    features: [
      "Original Hardwood Floors",
      "Updated Kitchen",
      "Private Garden",
      "Front Porch",
      "Detached Studio",
    ],
    images: [
      "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop",
    ],
    agent: MOCK_AGENTS[3]!,
    neighborhood: "South Congress",
    listingDate: "2024-09-20",
    status: "for-sale",
  },
  {
    id: "prop-4",
    title: "Contemporary Hillside Villa",
    slug: "contemporary-hillside-villa",
    price: 1_750_000,
    address: "5500 Mountain Ridge Road",
    city: "Austin",
    state: "TX",
    zipCode: "78730",
    propertyType: "house",
    bedrooms: 6,
    bathrooms: 5,
    squareFeet: 5_500,
    lotSize: 20_000,
    yearBuilt: 2022,
    description:
      "Architectural masterpiece perched on a hilltop with sweeping Hill Country views. Features include a cantilevered deck, chef's kitchen, primary suite with spa bath, and a separate guest casita.",
    features: [
      "Hill Country Views",
      "Guest Casita",
      "Chef's Kitchen",
      "Spa Bathroom",
      "Solar Panels",
      "EV Charger",
    ],
    images: [
      "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop",
    ],
    agent: MOCK_AGENTS[0]!,
    neighborhood: "Westlake Hills",
    listingDate: "2024-11-10",
    status: "for-sale",
  },
  {
    id: "prop-5",
    title: "Urban Loft in East Side",
    slug: "urban-loft-east-side",
    price: 415_000,
    address: "200 East 6th Street, Unit 4B",
    city: "Austin",
    state: "TX",
    zipCode: "78702",
    propertyType: "apartment",
    bedrooms: 2,
    bathrooms: 2,
    squareFeet: 1_400,
    yearBuilt: 2019,
    description:
      "Industrial-chic loft with exposed brick, polished concrete floors, 14-foot ceilings, and a private balcony overlooking the East Side arts district. Building includes rooftop pool and co-working lounge.",
    features: [
      "Exposed Brick",
      "14-Foot Ceilings",
      "Rooftop Pool",
      "Co-Working Lounge",
      "Balcony",
    ],
    images: [
      "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop",
    ],
    agent: MOCK_AGENTS[1]!,
    neighborhood: "East Side",
    listingDate: "2024-10-28",
    status: "pending",
  },
  {
    id: "prop-6",
    title: "Classic Colonial on Maple Lane",
    slug: "classic-colonial-maple-lane",
    price: 680_000,
    address: "45 Maple Lane",
    city: "Austin",
    state: "TX",
    zipCode: "78703",
    propertyType: "townhouse",
    bedrooms: 4,
    bathrooms: 3.5,
    squareFeet: 3_200,
    lotSize: 8_000,
    yearBuilt: 2005,
    description:
      "Elegant colonial-style townhouse in a tree-lined neighborhood. Formal living and dining rooms, a sun-drenched family room, updated chef's kitchen, and a spacious primary suite. Community pool and tennis courts included.",
    features: [
      "Community Pool",
      "Tennis Courts",
      "Updated Kitchen",
      "Fireplace",
      "Two-Car Garage",
      "Fenced Yard",
    ],
    images: [
      "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop",
    ],
    agent: MOCK_AGENTS[2]!,
    neighborhood: "Tarrytown",
    listingDate: "2024-08-15",
    status: "sold",
  },
];

/**
 * Look up a single property by its URL slug.
 *
 * @param slug - The URL-friendly slug to search for.
 * @returns The matching Property, or undefined if not found.
 */
export function getPropertyBySlug(slug: string): Property | undefined {
  return MOCK_PROPERTIES.find((property) => property.slug === slug);
}

/**
 * Filter properties by their listing status.
 *
 * @param status - The PropertyStatus to filter by.
 * @returns An array of properties matching the given status.
 */
export function getPropertiesByStatus(status: PropertyStatus): Property[] {
  return MOCK_PROPERTIES.filter((property) => property.status === status);
}

/**
 * Return featured properties (the first 3 listings).
 *
 * @returns An array of up to 3 featured Property objects.
 */
export function getFeaturedProperties(): Property[] {
  return MOCK_PROPERTIES.slice(0, 3);
}
