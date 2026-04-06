/**
 * TypeScript interfaces for all domain data models used across the app.
 */

/** The type of a property listing. */
export type PropertyType = 'house' | 'condo' | 'townhouse' | 'apartment' | 'land';

/** The current status of a property listing. */
export type PropertyStatus = 'for-sale' | 'pending' | 'sold';

/** The preferred contact method for a form submission. */
export type PreferredContact = 'email' | 'phone' | 'either';

/** Social media links for an agent. */
export interface SocialLinks {
  linkedin?: string;
  twitter?: string;
  facebook?: string;
  instagram?: string;
}

/** Represents a real estate agent. */
export interface Agent {
  id: string;
  name: string;
  title: string;
  phone: string;
  email: string;
  photo: string;
  bio: string;
  specialties: string[];
  propertiesCount: number;
  rating: number;
  socialLinks: SocialLinks;
}

/** Represents a neighborhood or area. */
export interface Neighborhood {
  id: string;
  name: string;
  slug: string;
  city: string;
  state: string;
  description: string;
  image: string;
  averagePrice: number;
  walkScore: number;
  transitScore: number;
  highlights: string[];
  featuredProperties: string[];
}

/** Represents a property listing. */
export interface Property {
  id: string;
  title: string;
  slug: string;
  price: number;
  address: string;
  city: string;
  state: string;
  zipCode: string;
  propertyType: PropertyType;
  bedrooms: number;
  bathrooms: number;
  squareFeet: number;
  lotSize: number;
  yearBuilt: number;
  description: string;
  features: string[];
  images: string[];
  agent: Agent;
  neighborhood: Neighborhood;
  listingDate: string;
  status: PropertyStatus;
}

/** Data submitted via the contact form. */
export interface ContactFormData {
  name: string;
  email: string;
  phone: string;
  message: string;
  propertyId?: string;
  preferredContact: PreferredContact;
}
