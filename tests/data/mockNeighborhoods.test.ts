/**
 * Tests for mock neighborhood data and helper functions.
 *
 * Validates data integrity, image URL formats, and lookup behaviour.
 */

import { describe, it, expect } from 'vitest';
import {
  MOCK_NEIGHBORHOODS,
  getNeighborhoodBySlug,
  getNeighborhoodById,
} from '../../src/data/mockNeighborhoods';

describe('MOCK_NEIGHBORHOODS', () => {
  it('should contain exactly 6 neighborhoods', () => {
    expect(MOCK_NEIGHBORHOODS).toHaveLength(6);
  });

  it('should have unique IDs for every neighborhood', () => {
    const ids = MOCK_NEIGHBORHOODS.map((n) => n.id);
    const uniqueIds = new Set(ids);
    expect(uniqueIds.size).toBe(ids.length);
  });

  it('should have unique slugs for every neighborhood', () => {
    const slugs = MOCK_NEIGHBORHOODS.map((n) => n.slug);
    const uniqueSlugs = new Set(slugs);
    expect(uniqueSlugs.size).toBe(slugs.length);
  });

  it('should use Unsplash URLs for all neighborhood images', () => {
    for (const neighborhood of MOCK_NEIGHBORHOODS) {
      expect(neighborhood.image).toMatch(/^https:\/\/images\.unsplash\.com\/photo-/);
    }
  });

  it('should have non-empty name, description, city, and state', () => {
    for (const neighborhood of MOCK_NEIGHBORHOODS) {
      expect(neighborhood.name.length).toBeGreaterThan(0);
      expect(neighborhood.description.length).toBeGreaterThan(0);
      expect(neighborhood.city.length).toBeGreaterThan(0);
      expect(neighborhood.state.length).toBe(2);
    }
  });

  it('should have positive averagePrice', () => {
    for (const neighborhood of MOCK_NEIGHBORHOODS) {
      expect(neighborhood.averagePrice).toBeGreaterThan(0);
    }
  });

  it('should have walkScore between 0 and 100', () => {
    for (const neighborhood of MOCK_NEIGHBORHOODS) {
      expect(neighborhood.walkScore).toBeGreaterThanOrEqual(0);
      expect(neighborhood.walkScore).toBeLessThanOrEqual(100);
    }
  });

  it('should have transitScore between 0 and 100', () => {
    for (const neighborhood of MOCK_NEIGHBORHOODS) {
      expect(neighborhood.transitScore).toBeGreaterThanOrEqual(0);
      expect(neighborhood.transitScore).toBeLessThanOrEqual(100);
    }
  });

  it('should have at least one highlight per neighborhood', () => {
    for (const neighborhood of MOCK_NEIGHBORHOODS) {
      expect(neighborhood.highlights.length).toBeGreaterThanOrEqual(1);
    }
  });

  it('should have at least one featured property ID per neighborhood', () => {
    for (const neighborhood of MOCK_NEIGHBORHOODS) {
      expect(neighborhood.featuredPropertyIds.length).toBeGreaterThanOrEqual(1);
    }
  });
});

describe('getNeighborhoodBySlug', () => {
  it('should return the correct neighborhood for a known slug', () => {
    const neighborhood = getNeighborhoodBySlug('downtown-austin');
    expect(neighborhood).toBeDefined();
    expect(neighborhood!.id).toBe('hood-002');
    expect(neighborhood!.name).toBe('Downtown Austin');
  });

  it('should return the correct neighborhood for south-congress', () => {
    const neighborhood = getNeighborhoodBySlug('south-congress');
    expect(neighborhood).toBeDefined();
    expect(neighborhood!.id).toBe('hood-003');
  });

  it('should return undefined for an unknown slug', () => {
    const neighborhood = getNeighborhoodBySlug('nonexistent-area');
    expect(neighborhood).toBeUndefined();
  });
});

describe('getNeighborhoodById', () => {
  it('should return the correct neighborhood for a known ID', () => {
    const neighborhood = getNeighborhoodById('hood-001');
    expect(neighborhood).toBeDefined();
    expect(neighborhood!.name).toBe('Lake Austin');
  });

  it('should return undefined for an unknown ID', () => {
    const neighborhood = getNeighborhoodById('hood-999');
    expect(neighborhood).toBeUndefined();
  });
});
