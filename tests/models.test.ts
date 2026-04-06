/**
 * Tests for TypeScript data models.
 *
 * These tests verify that the type definitions are correctly exported
 * and that mock data conforms to the expected interfaces.
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

describe("Type models", () => {
  it("should create a valid Agent object", () => {
    const agent: Agent = {
      id: "test-agent",
      name: "Test Agent",
      title: "Senior Agent",
      phone: "(555) 000-0000",
      email: "test@example.com",
      photo: "https://example.com/photo.jpg",
      bio: "A test agent bio.",
      specialties: ["Testing"],
      propertiesCount: 5,
      rating: 4.5,
      socialLinks: { linkedin: "https://linkedin.com/in/test" },
    };

    expect(agent.id).toBe("test-agent");
    expect(agent.rating).toBeGreaterThanOrEqual(0);
    expect(agent.rating).toBeLessThanOrEqual(5);
  });

  it("should create a valid Neighborhood object", () => {
    const neighborhood: Neighborhood = {
      id: "test-neighborhood",
      name: "Testville",
      slug: "testville",
      city: "Test City",
      state: "TS",
      description: "A test neighborhood.",
      image: "https://example.com/neighborhood.jpg",
      averagePrice: 500000,
      walkScore: 80,
      transitScore: 60,
      highlights: ["Great for testing"],
      featuredProperties: ["prop-1"],
    };

    expect(neighborhood.slug).toBe("testville");
    expect(neighborhood.walkScore).toBeLessThanOrEqual(100);
  });

  it("should create a valid ContactFormData object", () => {
    const formData: ContactFormData = {
      name: "John Doe",
      email: "john@example.com",
      phone: "(555) 123-4567",
      message: "I am interested.",
      propertyId: "prop-1",
      preferredContact: "email",
    };

    expect(formData.name).toBe("John Doe");
    expect(formData.propertyId).toBe("prop-1");
  });

  it("should allow ContactFormData without optional propertyId", () => {
    const formData: ContactFormData = {
      name: "Jane Doe",
      email: "jane@example.com",
      phone: "",
      message: "General inquiry.",
      preferredContact: "either",
    };

    expect(formData.propertyId).toBeUndefined();
  });

  it("should accept all valid PropertyType values", () => {
    const types: PropertyType[] = [
      "house",
      "condo",
      "townhouse",
      "apartment",
      "land",
    ];
    expect(types).toHaveLength(5);
  });

  it("should accept all valid PropertyStatus values", () => {
    const statuses: PropertyStatus[] = ["for-sale", "pending", "sold"];
    expect(statuses).toHaveLength(3);
  });

  it("should accept all valid PreferredContact values", () => {
    const contacts: PreferredContact[] = ["email", "phone", "either"];
    expect(contacts).toHaveLength(3);
  });
});
