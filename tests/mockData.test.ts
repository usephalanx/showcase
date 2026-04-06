/**
 * Tests for mock data modules and their helper functions.
 *
 * Verifies that mock data is correctly structured and that lookup /
 * filter helpers return expected results.
 */

import { describe, it, expect } from "vitest";
import {
  MOCK_PROPERTIES,
  getPropertyBySlug,
  getPropertiesByStatus,
  getFeaturedProperties,
} from "../src/data/mockProperties";
import { MOCK_AGENTS, getAgentById } from "../src/data/mockAgents";
import {
  MOCK_NEIGHBORHOODS,
  getNeighborhoodBySlug,
} from "../src/data/mockNeighborhoods";

describe("MOCK_PROPERTIES", () => {
  it("should contain 6 properties", () => {
    expect(MOCK_PROPERTIES).toHaveLength(6);
  });

  it("should have unique IDs", () => {
    const ids = MOCK_PROPERTIES.map((p) => p.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it("should have unique slugs", () => {
    const slugs = MOCK_PROPERTIES.map((p) => p.slug);
    expect(new Set(slugs).size).toBe(slugs.length);
  });

  it("every property should have at least one image", () => {
    for (const property of MOCK_PROPERTIES) {
      expect(property.images.length).toBeGreaterThanOrEqual(1);
    }
  });

  it("every property should reference a valid agent", () => {
    for (const property of MOCK_PROPERTIES) {
      expect(property.agent).toBeDefined();
      expect(property.agent.id).toBeTruthy();
    }
  });

  it("every property should reference a valid neighborhood", () => {
    for (const property of MOCK_PROPERTIES) {
      expect(property.neighborhood).toBeDefined();
      expect(property.neighborhood.id).toBeTruthy();
    }
  });
});

describe("getPropertyBySlug", () => {
  it("should find a property by its slug", () => {
    const result = getPropertyBySlug("modern-downtown-loft");
    expect(result).toBeDefined();
    expect(result?.id).toBe("prop-1");
  });

  it("should return undefined for a non-existent slug", () => {
    const result = getPropertyBySlug("non-existent-slug");
    expect(result).toBeUndefined();
  });
});

describe("getPropertiesByStatus", () => {
  it("should return properties with for-sale status", () => {
    const forSale = getPropertiesByStatus("for-sale");
    expect(forSale.length).toBeGreaterThan(0);
    for (const p of forSale) {
      expect(p.status).toBe("for-sale");
    }
  });

  it("should return properties with pending status", () => {
    const pending = getPropertiesByStatus("pending");
    expect(pending.length).toBeGreaterThanOrEqual(1);
    for (const p of pending) {
      expect(p.status).toBe("pending");
    }
  });

  it("should return empty array for sold status (none in mock data)", () => {
    const sold = getPropertiesByStatus("sold");
    expect(sold).toHaveLength(0);
  });
});

describe("getFeaturedProperties", () => {
  it("should return exactly 3 properties", () => {
    const featured = getFeaturedProperties();
    expect(featured).toHaveLength(3);
  });

  it("should return the first 3 properties from the list", () => {
    const featured = getFeaturedProperties();
    expect(featured[0].id).toBe(MOCK_PROPERTIES[0].id);
    expect(featured[1].id).toBe(MOCK_PROPERTIES[1].id);
    expect(featured[2].id).toBe(MOCK_PROPERTIES[2].id);
  });
});

describe("MOCK_AGENTS", () => {
  it("should contain 4 agents", () => {
    expect(MOCK_AGENTS).toHaveLength(4);
  });

  it("should have unique IDs", () => {
    const ids = MOCK_AGENTS.map((a) => a.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it("every agent should have a rating between 0 and 5", () => {
    for (const agent of MOCK_AGENTS) {
      expect(agent.rating).toBeGreaterThanOrEqual(0);
      expect(agent.rating).toBeLessThanOrEqual(5);
    }
  });
});

describe("getAgentById", () => {
  it("should find an agent by ID", () => {
    const result = getAgentById("agent-1");
    expect(result).toBeDefined();
    expect(result?.name).toBe("James Mitchell");
  });

  it("should return undefined for a non-existent ID", () => {
    const result = getAgentById("agent-999");
    expect(result).toBeUndefined();
  });
});

describe("MOCK_NEIGHBORHOODS", () => {
  it("should contain 4 neighborhoods", () => {
    expect(MOCK_NEIGHBORHOODS).toHaveLength(4);
  });

  it("should have unique slugs", () => {
    const slugs = MOCK_NEIGHBORHOODS.map((n) => n.slug);
    expect(new Set(slugs).size).toBe(slugs.length);
  });

  it("every neighborhood should have walk and transit scores in 0-100", () => {
    for (const n of MOCK_NEIGHBORHOODS) {
      expect(n.walkScore).toBeGreaterThanOrEqual(0);
      expect(n.walkScore).toBeLessThanOrEqual(100);
      expect(n.transitScore).toBeGreaterThanOrEqual(0);
      expect(n.transitScore).toBeLessThanOrEqual(100);
    }
  });
});

describe("getNeighborhoodBySlug", () => {
  it("should find a neighborhood by slug", () => {
    const result = getNeighborhoodBySlug("downtown-heights");
    expect(result).toBeDefined();
    expect(result?.id).toBe("neighborhood-1");
  });

  it("should return undefined for a non-existent slug", () => {
    const result = getNeighborhoodBySlug("no-such-place");
    expect(result).toBeUndefined();
  });
});
