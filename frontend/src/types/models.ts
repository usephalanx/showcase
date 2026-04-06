export type PropertyType = 'house' | 'condo' | 'townhouse' | 'apartment' | 'land';

export type PropertyStatus = 'for-sale' | 'pending' | 'sold';

export type PreferredContact = 'email' | 'phone' | 'either';

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
  socialLinks?: Record<string, string>;
}

export interface Neighborhood {
  id: string;
  name: string;
  slug: string;
  city: string;
  state: string;
  description: string;
  image: string;
  averagePrice: number;
  propertyCount: number;
  walkScore?: number;
  transitScore?: number;
  highlights: string[];
  featuredProperties?: string[];
}

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
  lotSize?: number;
  yearBuilt: number;
  description: string;
  features: string[];
  images: string[];
  agent: Agent;
  neighborhood: string;
  listingDate: string;
  status: PropertyStatus;
}

export interface ContactFormData {
  name: string;
  email: string;
  phone: string;
  message: string;
  propertyId?: string;
  preferredContact: PreferredContact;
}
