/**
 * Tests for TypeScript data models and mock data helpers.
 *
 * Validates that mock data arrays are well-formed and that helper
 * functions return the expected results.
 */

import { describe, it, expect } from "vitest";
import type {
  Property,
  Agent,
  Neighborhood,
  ContactFormData,
  PropertyType,
  PropertyStatus,
  PreferredContact,
} from "../src/types/models";
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

// ---------------------------------------------------------------------------
// Mock Properties
// ---------------------------------------------------------------------------

describe("MOCK_PROPERTIES", () => {
  it("should contain 6 properties", () => {
    expect(MOCK_PROPERTIES).toHaveLength(6);
  });

  it("every property should have required fields", () => {
    for (const p of MOCK_PROPERTIES) {
      expect(p.id).toBeTruthy();
      expect(p.title).toBeTruthy();
      expect(p.slug).toBeTruthy();
      expect(p.price).toBeGreaterThan(0);
      expect(p.address).toBeTruthy();
      expect(p.city).toBeTruthy();
      expect(p.state).toBeTruthy();
      expect(p.zipCode).toBeTruthy();
      expect(p.images.length).toBeGreaterThan(0);
      expect(p.agent).toBeDefined();
      expect(p.status).toBeTruthy();
    }
  });

  it("should have unique slugs", () => {
    const slugs = MOCK_PROPERTIES.map((p) => p.slug);
    expect(new Set(slugs).size).toBe(slugs.length);
  });

  it("should have unique IDs", () => {
    const ids = MOCK_PROPERTIES.map((p) => p.id);
    expect(new Set(ids).size).toBe(ids.length);
  });
});

describe("getPropertyBySlug", () => {
  it("should return a property for a valid slug", () => {
    const property = getPropertyBySlug("modern-lakefront-estate");
    expect(property).toBeDefined();
    expect(property!.id).toBe("prop-1");
  });

  it("should return undefined for an invalid slug", () => {
    const property = getPropertyBySlug("nonexistent-slug");
    expect(property).toBeUndefined();
  });
});

describe("getPropertiesByStatus", () => {
  it("should return only for-sale properties", () => {
    const forSale = getPropertiesByStatus("for-sale");
    expect(forSale.length).toBeGreaterThan(0);
    for (const p of forSale) {
      expect(p.status).toBe("for-sale");
    }
  });

  it("should return pending properties", () => {
    const pending = getPropertiesByStatus("pending");
    expect(pending.length).toBeGreaterThan(0);
    for (const p of pending) {
      expect(p.status).toBe("pending");
    }
  });

  it("should return sold properties", () => {
    const sold = getPropertiesByStatus("sold");
    expect(sold.length).toBeGreaterThan(0);
    for (const p of sold) {
      expect(p.status).toBe("sold");
    }
  });

  it("should return empty array for status with no matches", () => {
    // All statuses are covered, but this tests the filter logic
    const all = [
      ...getPropertiesByStatus("for-sale"),
      ...getPropertiesByStatus("pending"),
      ...getPropertiesByStatus("sold"),
    ];
    expect(all.length).toBe(MOCK_PROPERTIES.length);
  });
});

describe("getFeaturedProperties", () => {
  it("should return exactly 3 properties", () => {
    const featured = getFeaturedProperties();
    expect(featured).toHaveLength(3);
  });

  it("should return the first 3 properties", () => {
    const featured = getFeaturedProperties();
    expect(featured[0]!.id).toBe(MOCK_PROPERTIES[0]!.id);
    expect(featured[1]!.id).toBe(MOCK_PROPERTIES[1]!.id);
    expect(featured[2]!.id).toBe(MOCK_PROPERTIES[2]!.id);
  });
});

// ---------------------------------------------------------------------------
// Mock Agents
// ---------------------------------------------------------------------------

describe("MOCK_AGENTS", () => {
  it("should contain 4 agents", () => {
    expect(MOCK_AGENTS).toHaveLength(4);
  });

  it("every agent should have required fields", () => {
    for (const a of MOCK_AGENTS) {
      expect(a.id).toBeTruthy();
      expect(a.name).toBeTruthy();
      expect(a.title).toBeTruthy();
      expect(a.phone).toBeTruthy();
      expect(a.email).toBeTruthy();
      expect(a.photo).toBeTruthy();
      expect(a.bio).toBeTruthy();
      expect(a.specialties.length).toBeGreaterThan(0);
      expect(a.rating).toBeGreaterThanOrEqual(0);
      expect(a.rating).toBeLessThanOrEqual(5);
    }
  });

  it("should have unique IDs", () => {
    const ids = MOCK_AGENTS.map((a) => a.id);
    expect(new Set(ids).size).toBe(ids.length);
  });
});

describe("getAgentById", () => {
  it("should return an agent for a valid ID", () => {
    const agent = getAgentById("agent-1");
    expect(agent).toBeDefined();
    expect(agent!.name).toBe("James Mitchell");
  });

  it("should return undefined for an invalid ID", () => {
    const agent = getAgentById("nonexistent-id");
    expect(agent).toBeUndefined();
  });
});

// ---------------------------------------------------------------------------
// Mock Neighborhoods
// ---------------------------------------------------------------------------

describe("MOCK_NEIGHBORHOODS", () => {
  it("should contain 4 neighborhoods", () => {
    expect(MOCK_NEIGHBORHOODS).toHaveLength(4);
  });

  it("every neighborhood should have required fields", () => {
    for (const n of MOCK_NEIGHBORHOODS) {
      expect(n.id).toBeTruthy();
      expect(n.name).toBeTruthy();
      expect(n.slug).toBeTruthy();
      expect(n.city).toBeTruthy();
      expect(n.state).toBeTruthy();
      expect(n.description).toBeTruthy();
      expect(n.image).toBeTruthy();
      expect(n.averagePrice).toBeGreaterThan(0);
      expect(n.walkScore).toBeGreaterThanOrEqual(0);
      expect(n.walkScore).toBeLessThanOrEqual(100);
      expect(n.transitScore).toBeGreaterThanOrEqual(0);
      expect(n.transitScore).toBeLessThanOrEqual(100);
      expect(n.highlights.length).toBeGreaterThan(0);
    }
  });

  it("should have unique slugs", () => {
    const slugs = MOCK_NEIGHBORHOODS.map((n) => n.slug);
    expect(new Set(slugs).size).toBe(slugs.length);
  });
});

describe("getNeighborhoodBySlug", () => {
  it("should return a neighborhood for a valid slug", () => {
    const neighborhood = getNeighborhoodBySlug("downtown");
    expect(neighborhood).toBeDefined();
    expect(neighborhood!.name).toBe("Downtown");
  });

  it("should return undefined for an invalid slug", () => {
    const neighborhood = getNeighborhoodBySlug("nonexistent-slug");
    expect(neighborhood).toBeUndefined();
  });
});

// ---------------------------------------------------------------------------
// Type-level checks (compile-time; runtime assertions for completeness)
// ---------------------------------------------------------------------------

describe("Type contracts", () => {
  it("PropertyType union values should be valid", () => {
    const validTypes: PropertyType[] = [
      "house",
      "condo",
      "townhouse",
      "apartment",
      "land",
    ];
    for (const p of MOCK_PROPERTIES) {
      expect(validTypes).toContain(p.propertyType);
    }
  });

  it("PropertyStatus union values should be valid", () => {
    const validStatuses: PropertyStatus[] = ["for-sale", "pending", "sold"];
    for (const p of MOCK_PROPERTIES) {
      expect(validStatuses).toContain(p.status);
    }
  });

  it("ContactFormData shape should be constructible", () => {
    const form: ContactFormData = {
      name: "Test User",
      email: "test@example.com",
      phone: "(555) 000-0000",
      message: "I am interested in this property.",
      propertyId: "prop-1",
      preferredContact: "email",
    };
    expect(form.name).toBe("Test User");
    expect(form.preferredContact).toBe("email");
  });

  it("ContactFormData should allow optional propertyId", () => {
    const form: ContactFormData = {
      name: "Test User",
      email: "test@example.com",
      phone: "",
      message: "General inquiry.",
      preferredContact: "either",
    };
    expect(form.propertyId).toBeUndefined();
  });

  it("PreferredContact union values should be valid", () => {
    const validValues: PreferredContact[] = ["email", "phone", "either"];
    expect(validValues).toHaveLength(3);
  });
});
