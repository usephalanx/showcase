/**
 * Shared TypeScript interfaces for the Maddie Real Estate landing page.
 */

/** Represents a navigation link item. */
export interface NavLink {
  /** Display label for the link. */
  label: string;
  /** Target section ID (without the '#' prefix). */
  href: string;
}

/** Represents a property listing card. */
export interface Property {
  /** Unique identifier for the property. */
  id: string;
  /** Street address of the property. */
  address: string;
  /** Sale price formatted as a display string (e.g. "$1,250,000"). */
  price: string;
  /** Number of bedrooms. */
  bedrooms: number;
  /** Number of bathrooms. */
  bathrooms: number;
  /** Square footage of the property. */
  sqft: number;
  /** URL to the property image. */
  imageUrl: string;
  /** Status of the listing. */
  status: 'sold' | 'active' | 'pending';
}

/** Represents the agent's profile information. */
export interface AgentProfile {
  /** Agent's full name. */
  name: string;
  /** Professional title or designation. */
  title: string;
  /** Short biography paragraph. */
  bio: string;
  /** URL to the agent's headshot photo. */
  imageUrl: string;
  /** Phone number for contact. */
  phone: string;
  /** Email address for contact. */
  email: string;
}

/** Props interface for the PropertyCard component. */
export interface PropertyCardProps {
  /** The property data to display. */
  property: Property;
}

/** Contact form field values. */
export interface ContactFormData {
  /** Sender's full name. */
  name: string;
  /** Sender's email address. */
  email: string;
  /** Sender's phone number (optional). */
  phone?: string;
  /** Message body. */
  message: string;
}
