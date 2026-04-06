/**
 * Tests for TypeScript data models and mock data helpers.
 *
 * Run with: npx vitest run tests/test_models.ts
 */

import { describe, it, expect } from 'vitest';
import type { Property, Agent, Neighborhood, ContactFormData } from '../src/types/models';
import { MOCK_PROPERTIES, getPropertyBySlug, getPropertiesByStatus, getFeaturedProperties } from '../src/data/mockProperties';
import { MOCK_AGENTS, getAgentById } from '../src/data/mockAgents';
import { MOCK_NEIGHBORHOODS, getNeighborhoodById, getNeighborhoodBySlug } from '../src/data/mockNeighborhoods';

describe('Mock Properties', () => {
  it('should contain 6 properties', () => {
    expect(MOCK_PROPERTIES).toHaveLength(6);
  });

  it('each property should have required fields', () => {
    MOCK_PROPERTIES.forEach((property: Property) => {
      expect(property.id).toBeTruthy();
      expect(property.title).toBeTruthy();
      expect(property.slug).toBeTruthy();
      expect(property.price).toBeGreaterThan(0);
      expect(property.address).toBeTruthy();
      expect(property.city).toBeTruthy();
      expect(property.state).toBeTruthy();
      expect(property.zipCode).toBeTruthy();
      expect(property.images.length).toBeGreaterThan(0);
      expect(property.agent).toBeDefined();
      expect(property.neighborhood).toBeDefined();
    });
  });

  it('getPropertyBySlug should return the correct property', () => {
    const property = getPropertyBySlug('modern-farmhouse-open-floor-plan');
    expect(property).toBeDefined();
    expect(property!.id).toBe('prop-1');
  });

  it('getPropertyBySlug should return undefined for unknown slug', () => {
    const property = getPropertyBySlug('non-existent-property');
    expect(property).toBeUndefined();
  });

  it('getPropertiesByStatus should filter correctly', () => {
    const forSale = getPropertiesByStatus('for-sale');
    expect(forSale.length).toBeGreaterThan(0);
    forSale.forEach((p) => expect(p.status).toBe('for-sale'));

    const sold = getPropertiesByStatus('sold');
    expect(sold.length).toBeGreaterThan(0);
    sold.forEach((p) => expect(p.status).toBe('sold'));

    const pending = getPropertiesByStatus('pending');
    expect(pending.length).toBeGreaterThan(0);
    pending.forEach((p) => expect(p.status).toBe('pending'));
  });

  it('getFeaturedProperties should return the first 3 properties', () => {
    const featured = getFeaturedProperties();
    expect(featured).toHaveLength(3);
    expect(featured[0].id).toBe('prop-1');
    expect(featured[1].id).toBe('prop-2');
    expect(featured[2].id).toBe('prop-3');
  });
});

describe('Mock Agents', () => {
  it('should contain 4 agents', () => {
    expect(MOCK_AGENTS).toHaveLength(4);
  });

  it('each agent should have required fields', () => {
    MOCK_AGENTS.forEach((agent: Agent) => {
      expect(agent.id).toBeTruthy();
      expect(agent.name).toBeTruthy();
      expect(agent.email).toBeTruthy();
      expect(agent.phone).toBeTruthy();
      expect(agent.photo).toBeTruthy();
      expect(agent.rating).toBeGreaterThan(0);
      expect(agent.rating).toBeLessThanOrEqual(5);
    });
  });

  it('getAgentById should return the correct agent', () => {
    const agent = getAgentById('agent-1');
    expect(agent).toBeDefined();
    expect(agent!.name).toBe('James Mitchell');
  });

  it('getAgentById should return undefined for unknown id', () => {
    const agent = getAgentById('unknown-agent');
    expect(agent).toBeUndefined();
  });
});

describe('Mock Neighborhoods', () => {
  it('should contain 4 neighborhoods', () => {
    expect(MOCK_NEIGHBORHOODS).toHaveLength(4);
  });

  it('each neighborhood should have required fields', () => {
    MOCK_NEIGHBORHOODS.forEach((neighborhood: Neighborhood) => {
      expect(neighborhood.id).toBeTruthy();
      expect(neighborhood.name).toBeTruthy();
      expect(neighborhood.slug).toBeTruthy();
      expect(neighborhood.city).toBeTruthy();
      expect(neighborhood.state).toBeTruthy();
      expect(neighborhood.image).toBeTruthy();
      expect(neighborhood.averagePrice).toBeGreaterThan(0);
      expect(neighborhood.walkScore).toBeGreaterThanOrEqual(0);
      expect(neighborhood.walkScore).toBeLessThanOrEqual(100);
    });
  });

  it('getNeighborhoodById should return the correct neighborhood', () => {
    const neighborhood = getNeighborhoodById('neighborhood-1');
    expect(neighborhood).toBeDefined();
    expect(neighborhood!.name).toBe('Maple Heights');
  });

  it('getNeighborhoodById should return undefined for unknown id', () => {
    const neighborhood = getNeighborhoodById('unknown');
    expect(neighborhood).toBeUndefined();
  });

  it('getNeighborhoodBySlug should return the correct neighborhood', () => {
    const neighborhood = getNeighborhoodBySlug('riverside-district');
    expect(neighborhood).toBeDefined();
    expect(neighborhood!.id).toBe('neighborhood-2');
  });

  it('getNeighborhoodBySlug should return undefined for unknown slug', () => {
    const neighborhood = getNeighborhoodBySlug('nonexistent');
    expect(neighborhood).toBeUndefined();
  });
});

describe('ContactFormData type', () => {
  it('should accept valid contact form data', () => {
    const formData: ContactFormData = {
      name: 'John Doe',
      email: 'john@example.com',
      phone: '555-123-4567',
      message: 'I am interested in a property.',
      preferredContact: 'email',
    };
    expect(formData.name).toBe('John Doe');
    expect(formData.propertyId).toBeUndefined();
  });

  it('should accept contact form data with optional propertyId', () => {
    const formData: ContactFormData = {
      name: 'Jane Smith',
      email: 'jane@example.com',
      phone: '555-987-6543',
      message: 'Tell me more about this property.',
      propertyId: 'prop-1',
      preferredContact: 'phone',
    };
    expect(formData.propertyId).toBe('prop-1');
  });
});
