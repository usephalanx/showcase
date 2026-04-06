/**
 * Tests for mock property data and helper functions.
 *
 * Validates data integrity, image URL formats, and lookup/filter behaviour.
 */

import { describe, it, expect } from 'vitest';
import {
  MOCK_PROPERTIES,
  getPropertyBySlug,
  getPropertiesByStatus,
  getFeaturedProperties,
  getPropertyById,
  getPropertiesByNeighborhood,
  getPropertiesByAgent,
} from '../../src/data/mockProperties';

describe('MOCK_PROPERTIES', () => {
  it('should contain at least 12 properties', () => {
    expect(MOCK_PROPERTIES.length).toBeGreaterThanOrEqual(12);
  });

  it('should have unique IDs for every property', () => {
    const ids = MOCK_PROPERTIES.map((p) => p.id);
    const uniqueIds = new Set(ids);
    expect(uniqueIds.size).toBe(ids.length);
  });

  it('should have unique slugs for every property', () => {
    const slugs = MOCK_PROPERTIES.map((p) => p.slug);
    const uniqueSlugs = new Set(slugs);
    expect(uniqueSlugs.size).toBe(slugs.length);
  });

  it('should have at least one image per property', () => {
    for (const property of MOCK_PROPERTIES) {
      expect(property.images.length).toBeGreaterThanOrEqual(1);
    }
  });

  it('should use Unsplash URLs for all images', () => {
    for (const property of MOCK_PROPERTIES) {
      for (const img of property.images) {
        expect(img).toMatch(/^https:\/\/images\.unsplash\.com\/photo-/);
      }
    }
  });

  it('should have valid price values (positive numbers)', () => {
    for (const property of MOCK_PROPERTIES) {
      expect(property.price).toBeGreaterThan(0);
    }
  });

  it('should have valid bedroom counts (non-negative)', () => {
    for (const property of MOCK_PROPERTIES) {
      expect(property.bedrooms).toBeGreaterThanOrEqual(0);
    }
  });

  it('should have valid bathroom counts (positive)', () => {
    for (const property of MOCK_PROPERTIES) {
      expect(property.bathrooms).toBeGreaterThan(0);
    }
  });

  it('should have valid squareFeet (positive)', () => {
    for (const property of MOCK_PROPERTIES) {
      expect(property.squareFeet).toBeGreaterThan(0);
    }
  });

  it('should have valid yearBuilt (>= 1800)', () => {
    for (const property of MOCK_PROPERTIES) {
      expect(property.yearBuilt).toBeGreaterThanOrEqual(1800);
    }
  });

  it('should have valid status values', () => {
    const validStatuses = new Set(['for-sale', 'pending', 'sold']);
    for (const property of MOCK_PROPERTIES) {
      expect(validStatuses.has(property.status)).toBe(true);
    }
  });

  it('should have valid propertyType values', () => {
    const validTypes = new Set(['house', 'condo', 'townhouse', 'apartment', 'land']);
    for (const property of MOCK_PROPERTIES) {
      expect(validTypes.has(property.propertyType)).toBe(true);
    }
  });
});

describe('getPropertyBySlug', () => {
  it('should return the correct property for a known slug', () => {
    const property = getPropertyBySlug('modern-lakefront-estate');
    expect(property).toBeDefined();
    expect(property!.id).toBe('prop-001');
  });

  it('should return undefined for an unknown slug', () => {
    const property = getPropertyBySlug('nonexistent-slug');
    expect(property).toBeUndefined();
  });
});

describe('getPropertiesByStatus', () => {
  it('should return only for-sale properties', () => {
    const forSale = getPropertiesByStatus('for-sale');
    expect(forSale.length).toBeGreaterThan(0);
    for (const p of forSale) {
      expect(p.status).toBe('for-sale');
    }
  });

  it('should return only pending properties', () => {
    const pending = getPropertiesByStatus('pending');
    expect(pending.length).toBeGreaterThan(0);
    for (const p of pending) {
      expect(p.status).toBe('pending');
    }
  });

  it('should return only sold properties', () => {
    const sold = getPropertiesByStatus('sold');
    expect(sold.length).toBeGreaterThan(0);
    for (const p of sold) {
      expect(p.status).toBe('sold');
    }
  });
});

describe('getFeaturedProperties', () => {
  it('should return at most 3 properties', () => {
    const featured = getFeaturedProperties();
    expect(featured.length).toBeLessThanOrEqual(3);
  });

  it('should return only featured properties', () => {
    const featured = getFeaturedProperties();
    for (const p of featured) {
      expect(p.featured).toBe(true);
    }
  });

  it('should return at least 1 featured property', () => {
    const featured = getFeaturedProperties();
    expect(featured.length).toBeGreaterThanOrEqual(1);
  });
});

describe('getPropertyById', () => {
  it('should return the correct property for a known ID', () => {
    const property = getPropertyById('prop-003');
    expect(property).toBeDefined();
    expect(property!.slug).toBe('charming-craftsman-bungalow');
  });

  it('should return undefined for an unknown ID', () => {
    const property = getPropertyById('prop-999');
    expect(property).toBeUndefined();
  });
});

describe('getPropertiesByNeighborhood', () => {
  it('should return properties in the given neighborhood', () => {
    const properties = getPropertiesByNeighborhood('hood-003');
    expect(properties.length).toBeGreaterThan(0);
    for (const p of properties) {
      expect(p.neighborhoodId).toBe('hood-003');
    }
  });

  it('should return empty array for unknown neighborhood', () => {
    const properties = getPropertiesByNeighborhood('hood-999');
    expect(properties).toEqual([]);
  });
});

describe('getPropertiesByAgent', () => {
  it('should return properties listed by the given agent', () => {
    const properties = getPropertiesByAgent('agent-001');
    expect(properties.length).toBeGreaterThan(0);
    for (const p of properties) {
      expect(p.agentId).toBe('agent-001');
    }
  });

  it('should return empty array for unknown agent', () => {
    const properties = getPropertiesByAgent('agent-999');
    expect(properties).toEqual([]);
  });
});
