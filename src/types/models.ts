/**
 * Domain data models for the real estate website.
 *
 * All interfaces and type aliases used across the application are
 * defined here as a single source of truth.
 */

/** The type classification of a property listing. */
export type PropertyType = "house" | "condo" | "townhouse" | "apartment" | "land";

/** The current sale status of a property listing. */
export type PropertyStatus = "for-sale" | "pending" | "sold";

/** The user's preferred method of contact. */
export type PreferredContact = "email" | "phone" | "either";

/** Social media links for an agent profile. */
export interface SocialLinks {
  /** LinkedIn profile URL. */
  linkedin?: string;
  /** Twitter / X profile URL. */
  twitter?: string;
  /** Facebook profile URL. */
  facebook?: string;
  /** Instagram profile URL. */
  instagram?: string;
}

/**
 * Represents a real estate agent.
 */
export interface Agent {
  /** Unique identifier. */
  id: string;
  /** Full display name. */
  name: string;
  /** Professional title (e.g. "Senior Agent"). */
  title: string;
  /** Contact phone number. */
  phone: string;
  /** Contact email address. */
  email: string;
  /** URL to a profile photo. */
  photo: string;
  /** Short biography. */
  bio: string;
  /** List of market specialties. */
  specialties: string[];
  /** Number of active property listings. */
  propertiesCount: number;
  /** Average client rating (0–5). */
  rating: number;
  /** Optional social media links. */
  socialLinks: SocialLinks;
}

/**
 * Represents a neighborhood or area.
 */
export interface Neighborhood {
  /** Unique identifier. */
  id: string;
  /** Display name. */
  name: string;
  /** URL-friendly slug. */
  slug: string;
  /** City where the neighborhood is located. */
  city: string;
  /** State abbreviation. */
  state: string;
  /** Narrative description. */
  description: string;
  /** Hero image URL. */
  image: string;
  /** Average listing price in the area. */
  averagePrice: number;
  /** Walk Score (0–100). */
  walkScore: number;
  /** Transit Score (0–100). */
  transitScore: number;
  /** Notable highlights of the area. */
  highlights: string[];
  /** IDs of featured properties in this neighborhood. */
  featuredProperties: string[];
}

/**
 * Represents a property listing.
 */
export interface Property {
  /** Unique identifier. */
  id: string;
  /** Listing headline / title. */
  title: string;
  /** URL-friendly slug. */
  slug: string;
  /** Listing price in USD. */
  price: number;
  /** Street address. */
  address: string;
  /** City. */
  city: string;
  /** State abbreviation. */
  state: string;
  /** ZIP code. */
  zipCode: string;
  /** Classification of the property. */
  propertyType: PropertyType;
  /** Number of bedrooms. */
  bedrooms: number;
  /** Number of bathrooms (supports half-baths as 0.5). */
  bathrooms: number;
  /** Interior square footage. */
  squareFeet: number;
  /** Lot size in acres (optional for condos, etc.). */
  lotSize?: number;
  /** Year the property was built. */
  yearBuilt: number;
  /** Full description of the property. */
  description: string;
  /** List of notable features / amenities. */
  features: string[];
  /** Gallery image URLs. */
  images: string[];
  /** The listing agent. */
  agent: Agent;
  /** The neighborhood the property belongs to. */
  neighborhood: Neighborhood;
  /** ISO-8601 date string when the listing was published. */
  listingDate: string;
  /** Current sale status. */
  status: PropertyStatus;
}

/**
 * Data captured from the contact / inquiry form.
 */
export interface ContactFormData {
  /** Full name of the person submitting the form. */
  name: string;
  /** Email address. */
  email: string;
  /** Phone number (optional). */
  phone: string;
  /** Free-text message body. */
  message: string;
  /** ID of the property the inquiry is about (optional). */
  propertyId?: string;
  /** How the user prefers to be contacted. */
  preferredContact: PreferredContact;
}
