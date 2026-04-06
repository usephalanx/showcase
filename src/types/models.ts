/**
 * Domain data models for the real estate website.
 *
 * All TypeScript interfaces and type aliases used across the application
 * are defined here as the single source of truth.
 */

/** The kind of real estate property. */
export type PropertyType = "house" | "condo" | "townhouse" | "apartment" | "land";

/** Current listing status of a property. */
export type PropertyStatus = "for-sale" | "pending" | "sold";

/** How the user prefers to be contacted. */
export type PreferredContact = "email" | "phone" | "either";

/** Social media links for an agent profile. */
export interface SocialLinks {
  /** LinkedIn profile URL. */
  linkedin?: string;
  /** Twitter/X profile URL. */
  twitter?: string;
  /** Facebook profile URL. */
  facebook?: string;
  /** Instagram profile URL. */
  instagram?: string;
}

/** A real estate agent. */
export interface Agent {
  /** Unique identifier. */
  id: string;
  /** Full display name. */
  name: string;
  /** Professional title (e.g., "Senior Real Estate Agent"). */
  title: string;
  /** Contact phone number. */
  phone: string;
  /** Contact email address. */
  email: string;
  /** URL to the agent's headshot photo. */
  photo: string;
  /** Short biography. */
  bio: string;
  /** List of specialisation areas. */
  specialties: string[];
  /** Number of properties currently managed. */
  propertiesCount: number;
  /** Average client rating (0–5). */
  rating: number;
  /** Optional social media links. */
  socialLinks: SocialLinks;
}

/** A property listing. */
export interface Property {
  /** Unique identifier. */
  id: string;
  /** Display title / headline. */
  title: string;
  /** URL-friendly slug derived from the title. */
  slug: string;
  /** Listing price in USD (whole dollars). */
  price: number;
  /** Street address. */
  address: string;
  /** City name. */
  city: string;
  /** State abbreviation. */
  state: string;
  /** ZIP / postal code. */
  zipCode: string;
  /** Type of property. */
  propertyType: PropertyType;
  /** Number of bedrooms. */
  bedrooms: number;
  /** Number of bathrooms (supports half-baths as 0.5). */
  bathrooms: number;
  /** Interior living area in square feet. */
  squareFeet: number;
  /** Total lot size in square feet (optional for condos). */
  lotSize?: number;
  /** Year the structure was built. */
  yearBuilt: number;
  /** Full-text description of the property. */
  description: string;
  /** Notable features / amenities. */
  features: string[];
  /** Ordered list of image URLs (first is the hero image). */
  images: string[];
  /** The listing agent. */
  agent: Agent;
  /** Name of the neighborhood this property belongs to. */
  neighborhood: string;
  /** ISO-8601 date string of when the listing was published. */
  listingDate: string;
  /** Current listing status. */
  status: PropertyStatus;
}

/** A neighborhood / area guide. */
export interface Neighborhood {
  /** Unique identifier. */
  id: string;
  /** Display name. */
  name: string;
  /** URL-friendly slug. */
  slug: string;
  /** City the neighborhood is in. */
  city: string;
  /** State abbreviation. */
  state: string;
  /** Descriptive overview of the area. */
  description: string;
  /** Hero image URL. */
  image: string;
  /** Median / average property price in the area. */
  averagePrice: number;
  /** Walk Score® (0–100). */
  walkScore: number;
  /** Transit Score® (0–100). */
  transitScore: number;
  /** Key neighbourhood highlights / selling points. */
  highlights: string[];
  /** IDs of featured properties in this neighborhood. */
  featuredProperties: string[];
}

/** Data submitted through the contact inquiry form. */
export interface ContactFormData {
  /** Full name of the person making the inquiry. */
  name: string;
  /** Email address. */
  email: string;
  /** Phone number (optional). */
  phone: string;
  /** Free-text message body. */
  message: string;
  /** Property ID the inquiry is about (if applicable). */
  propertyId?: string;
  /** How the user prefers to be reached. */
  preferredContact: PreferredContact;
}
