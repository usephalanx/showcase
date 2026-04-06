/**
 * Domain model type definitions for the real estate website.
 *
 * Every data structure used across the application is defined here to
 * ensure type safety and consistent contracts between components, pages,
 * and data layers.
 */

// ---------------------------------------------------------------------------
// Union / Literal Types
// ---------------------------------------------------------------------------

/** The category of a property listing. */
export type PropertyType = 'house' | 'condo' | 'townhouse' | 'apartment' | 'land';

/** Current sales status of a property. */
export type PropertyStatus = 'for-sale' | 'pending' | 'sold';

/** How the user prefers to be contacted. */
export type PreferredContact = 'email' | 'phone' | 'either';

// ---------------------------------------------------------------------------
// Core Interfaces
// ---------------------------------------------------------------------------

/** A real estate property listing. */
export interface Property {
  /** Unique identifier. */
  id: string;
  /** Display title shown in cards and detail pages. */
  title: string;
  /** URL-friendly slug derived from the title. */
  slug: string;
  /** Listing price in USD (whole dollars). */
  price: number;
  /** Street address line. */
  address: string;
  /** City name. */
  city: string;
  /** Two-letter US state abbreviation. */
  state: string;
  /** Five-digit ZIP code. */
  zipCode: string;
  /** Category of the property. */
  propertyType: PropertyType;
  /** Number of bedrooms. */
  bedrooms: number;
  /** Number of bathrooms (may include halves, e.g. 2.5). */
  bathrooms: number;
  /** Total interior square footage. */
  squareFeet: number;
  /** Lot size in acres (optional for condos / apartments). */
  lotSize?: number;
  /** Year the structure was built. */
  yearBuilt: number;
  /** Long-form marketing description. */
  description: string;
  /** Notable features / amenities. */
  features: string[];
  /** Ordered list of image URLs (first is hero). */
  images: string[];
  /** Whether this property should appear in the "featured" section. */
  featured: boolean;
  /** ID of the listing agent. */
  agentId: string;
  /** ID of the neighbourhood the property belongs to. */
  neighborhoodId: string;
  /** ISO-8601 date string of the original listing date. */
  listingDate: string;
  /** Current sales status. */
  status: PropertyStatus;
}

/** Social-media links for an agent. */
export interface SocialLinks {
  linkedin?: string;
  twitter?: string;
  instagram?: string;
  facebook?: string;
}

/** A real estate agent or broker. */
export interface Agent {
  /** Unique identifier. */
  id: string;
  /** Full display name. */
  name: string;
  /** Professional title (e.g. "Senior Listing Agent"). */
  title: string;
  /** Contact phone number. */
  phone: string;
  /** Contact email address. */
  email: string;
  /** Headshot / portrait image URL. */
  photo: string;
  /** Short biography paragraph. */
  bio: string;
  /** Areas of expertise. */
  specialties: string[];
  /** Total active listings count. */
  propertiesCount: number;
  /** Average client rating (1–5 scale). */
  rating: number;
  /** Optional social media links. */
  socialLinks: SocialLinks;
}

/** A neighbourhood or community area. */
export interface Neighborhood {
  /** Unique identifier. */
  id: string;
  /** Display name. */
  name: string;
  /** URL-friendly slug. */
  slug: string;
  /** City the neighbourhood is located in. */
  city: string;
  /** Two-letter US state abbreviation. */
  state: string;
  /** Marketing description. */
  description: string;
  /** Hero image URL. */
  image: string;
  /** Average listing price in USD. */
  averagePrice: number;
  /** Walk Score (0–100). */
  walkScore: number;
  /** Transit Score (0–100). */
  transitScore: number;
  /** Key highlights / selling points. */
  highlights: string[];
  /** IDs of featured properties within this neighbourhood. */
  featuredPropertyIds: string[];
}

/** Shape of the contact-us form submission payload. */
export interface ContactFormData {
  /** Sender's full name. */
  name: string;
  /** Sender's email address. */
  email: string;
  /** Sender's phone number (optional). */
  phone?: string;
  /** Free-text message body. */
  message: string;
  /** If the enquiry relates to a specific property. */
  propertyId?: string;
  /** How the sender would like to be reached. */
  preferredContact: PreferredContact;
}
