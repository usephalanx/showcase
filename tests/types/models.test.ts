/**
 * Type-level and runtime tests for domain model type definitions.
 *
 * Verifies that the TypeScript interfaces compile correctly and that
 * mock data conforms to the expected shapes.
 */

import { describe, it, expect } from 'vitest';
import type {
  Property,
  Agent,
  Neighborhood,
  ContactFormData,
  PropertyType,
  PropertyStatus,
  PreferredContact,
} from '../../src/types/models';

describe('Type definitions', () => {
  it('should allow a valid Property object', () => {
    const property: Property = {
      id: 'test-001',
      title: 'Test Property',
      slug: 'test-property',
      price: 500000,
      address: '123 Main St',
      city: 'Austin',
      state: 'TX',
      zipCode: '78701',
      propertyType: 'house',
      bedrooms: 3,
      bathrooms: 2,
      squareFeet: 1800,
      lotSize: 0.25,
      yearBuilt: 2020,
      description: 'A lovely test property.',
      features: ['Pool', 'Garage'],
      images: ['https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop'],
      featured: true,
      agentId: 'agent-001',
      neighborhoodId: 'hood-001',
      listingDate: '2024-01-01',
      status: 'for-sale',
    };

    expect(property.id).toBe('test-001');
    expect(property.bedrooms).toBe(3);
    expect(property.featured).toBe(true);
  });

  it('should allow a Property without optional lotSize', () => {
    const condo: Property = {
      id: 'test-002',
      title: 'Test Condo',
      slug: 'test-condo',
      price: 300000,
      address: '456 High St #10',
      city: 'Austin',
      state: 'TX',
      zipCode: '78702',
      propertyType: 'condo',
      bedrooms: 1,
      bathrooms: 1,
      squareFeet: 750,
      yearBuilt: 2019,
      description: 'A test condo.',
      features: [],
      images: [],
      featured: false,
      agentId: 'agent-002',
      neighborhoodId: 'hood-002',
      listingDate: '2024-02-01',
      status: 'pending',
    };

    expect(condo.lotSize).toBeUndefined();
    expect(condo.propertyType).toBe('condo');
  });

  it('should allow a valid Agent object', () => {
    const agent: Agent = {
      id: 'agent-test',
      name: 'Test Agent',
      title: 'Listing Agent',
      phone: '(512) 555-0000',
      email: 'test@example.com',
      photo: 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&h=400&fit=crop',
      bio: 'A great agent.',
      specialties: ['Luxury'],
      propertiesCount: 5,
      rating: 4.5,
      socialLinks: { linkedin: 'https://linkedin.com/in/test' },
    };

    expect(agent.name).toBe('Test Agent');
    expect(agent.rating).toBe(4.5);
  });

  it('should allow a valid Neighborhood object', () => {
    const neighborhood: Neighborhood = {
      id: 'hood-test',
      name: 'Test Neighborhood',
      slug: 'test-neighborhood',
      city: 'Austin',
      state: 'TX',
      description: 'A wonderful area.',
      image: 'https://images.unsplash.com/photo-1444723121867-7a241cacace9?w=800&h=600&fit=crop',
      averagePrice: 600000,
      walkScore: 75,
      transitScore: 50,
      highlights: ['Parks', 'Schools'],
      featuredPropertyIds: ['prop-001'],
    };

    expect(neighborhood.slug).toBe('test-neighborhood');
    expect(neighborhood.walkScore).toBe(75);
  });

  it('should allow a valid ContactFormData object', () => {
    const formData: ContactFormData = {
      name: 'John Doe',
      email: 'john@example.com',
      phone: '(512) 555-1234',
      message: 'I am interested in a property.',
      propertyId: 'prop-001',
      preferredContact: 'email',
    };

    expect(formData.name).toBe('John Doe');
    expect(formData.preferredContact).toBe('email');
  });

  it('should allow ContactFormData without optional fields', () => {
    const formData: ContactFormData = {
      name: 'Jane Smith',
      email: 'jane@example.com',
      message: 'General inquiry.',
      preferredContact: 'either',
    };

    expect(formData.phone).toBeUndefined();
    expect(formData.propertyId).toBeUndefined();
  });

  it('should accept all valid PropertyType values', () => {
    const types: PropertyType[] = ['house', 'condo', 'townhouse', 'apartment', 'land'];
    expect(types).toHaveLength(5);
  });

  it('should accept all valid PropertyStatus values', () => {
    const statuses: PropertyStatus[] = ['for-sale', 'pending', 'sold'];
    expect(statuses).toHaveLength(3);
  });

  it('should accept all valid PreferredContact values', () => {
    const contacts: PreferredContact[] = ['email', 'phone', 'either'];
    expect(contacts).toHaveLength(3);
  });
});
