/**
 * Mock property listing data for development and testing.
 *
 * Provides a static array of Property objects with Unsplash image URLs
 * and helper functions for common queries.
 */

import type { Property, PropertyStatus } from "../types/models";
import { MOCK_AGENTS } from "./mockAgents";
import { MOCK_NEIGHBORHOODS } from "./mockNeighborhoods";

/** Static list of mock property listings. */
export const MOCK_PROPERTIES: Property[] = [
  {
    id: "prop-1",
    title: "Modern Downtown Loft",
    slug: "modern-downtown-loft",
    price: 685000,
    address: "123 Main Street, Unit 4A",
    city: "Metropolis",
    state: "CA",
    zipCode: "90001",
    propertyType: "condo",
    bedrooms: 2,
    bathrooms: 2,
    squareFeet: 1450,
    lotSize: undefined,
    yearBuilt: 2019,
    description:
      "An open-concept loft in the heart of Downtown Heights featuring floor-to-ceiling windows, polished concrete floors, and designer finishes throughout. The chef's kitchen boasts quartz countertops and premium stainless steel appliances. Building amenities include a rooftop terrace, fitness center, and 24-hour concierge.",
    features: [
      "Floor-to-ceiling windows",
      "Polished concrete floors",
      "Quartz countertops",
      "Stainless steel appliances",
      "In-unit laundry",
      "Rooftop terrace access",
      "Fitness center",
      "1 parking space",
    ],
    images: [
      "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop",
    ],
    agent: MOCK_AGENTS[1],
    neighborhood: MOCK_NEIGHBORHOODS[0],
    listingDate: "2024-09-15",
    status: "for-sale",
  },
  {
    id: "prop-2",
    title: "Elegant Penthouse Suite",
    slug: "elegant-penthouse-suite",
    price: 1250000,
    address: "456 Skyline Boulevard, PH1",
    city: "Metropolis",
    state: "CA",
    zipCode: "90002",
    propertyType: "condo",
    bedrooms: 3,
    bathrooms: 3.5,
    squareFeet: 2800,
    lotSize: undefined,
    yearBuilt: 2021,
    description:
      "A breathtaking penthouse offering panoramic city views from every room. This residence features a private elevator entry, a wraparound terrace, a gourmet kitchen with a wine fridge, and a spa-like primary suite with heated floors.",
    features: [
      "Panoramic city views",
      "Private elevator entry",
      "Wraparound terrace",
      "Wine fridge",
      "Heated bathroom floors",
      "Smart home system",
      "2 parking spaces",
      "Concierge service",
    ],
    images: [
      "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop",
    ],
    agent: MOCK_AGENTS[0],
    neighborhood: MOCK_NEIGHBORHOODS[0],
    listingDate: "2024-10-01",
    status: "for-sale",
  },
  {
    id: "prop-3",
    title: "Charming Oakwood Family Home",
    slug: "charming-oakwood-family-home",
    price: 875000,
    address: "789 Elm Drive",
    city: "Metropolis",
    state: "CA",
    zipCode: "90003",
    propertyType: "house",
    bedrooms: 4,
    bathrooms: 3,
    squareFeet: 2600,
    lotSize: 0.35,
    yearBuilt: 2005,
    description:
      "A beautifully maintained family home on a quiet cul-de-sac in Oakwood Estates. Features include a sun-drenched open-plan living area, a landscaped backyard with a patio, and a two-car garage. Walking distance to award-winning schools and community parks.",
    features: [
      "Open-plan living area",
      "Landscaped backyard",
      "Covered patio",
      "Two-car garage",
      "Hardwood floors",
      "Updated kitchen",
      "Walk to schools",
      "Community pool access",
    ],
    images: [
      "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop",
    ],
    agent: MOCK_AGENTS[2],
    neighborhood: MOCK_NEIGHBORHOODS[1],
    listingDate: "2024-08-20",
    status: "for-sale",
  },
  {
    id: "prop-4",
    title: "Renovated Craftsman Bungalow",
    slug: "renovated-craftsman-bungalow",
    price: 720000,
    address: "321 Maple Lane",
    city: "Metropolis",
    state: "CA",
    zipCode: "90003",
    propertyType: "house",
    bedrooms: 3,
    bathrooms: 2,
    squareFeet: 1800,
    lotSize: 0.25,
    yearBuilt: 1948,
    description:
      "A lovingly renovated Craftsman bungalow that blends vintage charm with modern amenities. Original built-in cabinetry and wood beams are complemented by a brand-new kitchen, updated bathrooms, and energy-efficient windows.",
    features: [
      "Original wood beams",
      "Built-in cabinetry",
      "New kitchen",
      "Updated bathrooms",
      "Energy-efficient windows",
      "Front porch",
      "Detached garage",
      "Mature fruit trees",
    ],
    images: [
      "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop",
    ],
    agent: MOCK_AGENTS[3],
    neighborhood: MOCK_NEIGHBORHOODS[1],
    listingDate: "2024-07-10",
    status: "pending",
  },
  {
    id: "prop-5",
    title: "Waterfront Luxury Villa",
    slug: "waterfront-luxury-villa",
    price: 2150000,
    address: "10 Harbor Point Road",
    city: "Metropolis",
    state: "CA",
    zipCode: "90004",
    propertyType: "house",
    bedrooms: 5,
    bathrooms: 4.5,
    squareFeet: 4200,
    lotSize: 0.6,
    yearBuilt: 2017,
    description:
      "A stunning waterfront villa with unobstructed ocean views, an infinity pool, and a private dock. The open-concept great room flows seamlessly to an expansive outdoor living area. The gourmet kitchen features a 12-foot island, Sub-Zero refrigeration, and a Wolf range.",
    features: [
      "Ocean views",
      "Infinity pool",
      "Private dock",
      "Gourmet kitchen",
      "12-foot kitchen island",
      "Outdoor living area",
      "Three-car garage",
      "Smart home automation",
    ],
    images: [
      "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop",
    ],
    agent: MOCK_AGENTS[0],
    neighborhood: MOCK_NEIGHBORHOODS[2],
    listingDate: "2024-11-01",
    status: "for-sale",
  },
  {
    id: "prop-6",
    title: "Maplewood Modern Townhouse",
    slug: "maplewood-modern-townhouse",
    price: 540000,
    address: "55 Cedar Court",
    city: "Metropolis",
    state: "CA",
    zipCode: "90005",
    propertyType: "townhouse",
    bedrooms: 3,
    bathrooms: 2.5,
    squareFeet: 1950,
    lotSize: 0.1,
    yearBuilt: 2022,
    description:
      "A brand-new townhouse in the heart of Maplewood Commons. This three-story home features a rooftop deck, an attached garage, and an open-plan main level ideal for entertaining. High-end finishes include white-oak flooring, custom tile work, and designer lighting.",
    features: [
      "Rooftop deck",
      "Attached garage",
      "White-oak flooring",
      "Custom tile work",
      "Designer lighting",
      "Open-plan main level",
      "Walk to cafes and shops",
      "EV charger-ready",
    ],
    images: [
      "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop",
      "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop",
    ],
    agent: MOCK_AGENTS[3],
    neighborhood: MOCK_NEIGHBORHOODS[3],
    listingDate: "2024-10-15",
    status: "for-sale",
  },
];

/**
 * Retrieve a single property by its URL-friendly slug.
 *
 * @param slug - The property slug to look up.
 * @returns The matching Property object, or undefined if not found.
 */
export function getPropertyBySlug(slug: string): Property | undefined {
  return MOCK_PROPERTIES.find((p) => p.slug === slug);
}

/**
 * Filter properties by their sale status.
 *
 * @param status - The PropertyStatus to filter on.
 * @returns An array of properties matching the given status.
 */
export function getPropertiesByStatus(status: PropertyStatus): Property[] {
  return MOCK_PROPERTIES.filter((p) => p.status === status);
}

/**
 * Return the first three properties as "featured" listings.
 *
 * @returns An array of up to 3 featured Property objects.
 */
export function getFeaturedProperties(): Property[] {
  return MOCK_PROPERTIES.slice(0, 3);
}
