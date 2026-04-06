/**
 * Tests for mock agent data and helper functions.
 *
 * Validates data integrity, photo URL formats, and lookup behaviour.
 */

import { describe, it, expect } from 'vitest';
import { MOCK_AGENTS, getAgentById } from '../../src/data/mockAgents';

describe('MOCK_AGENTS', () => {
  it('should contain at least 3 agents', () => {
    expect(MOCK_AGENTS.length).toBeGreaterThanOrEqual(3);
  });

  it('should have unique IDs for every agent', () => {
    const ids = MOCK_AGENTS.map((a) => a.id);
    const uniqueIds = new Set(ids);
    expect(uniqueIds.size).toBe(ids.length);
  });

  it('should use Unsplash URLs for all agent photos', () => {
    for (const agent of MOCK_AGENTS) {
      expect(agent.photo).toMatch(/^https:\/\/images\.unsplash\.com\/photo-/);
    }
  });

  it('should have non-empty name, title, phone, email, and bio', () => {
    for (const agent of MOCK_AGENTS) {
      expect(agent.name.length).toBeGreaterThan(0);
      expect(agent.title.length).toBeGreaterThan(0);
      expect(agent.phone.length).toBeGreaterThan(0);
      expect(agent.email.length).toBeGreaterThan(0);
      expect(agent.bio.length).toBeGreaterThan(0);
    }
  });

  it('should have valid email format', () => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    for (const agent of MOCK_AGENTS) {
      expect(agent.email).toMatch(emailRegex);
    }
  });

  it('should have at least one specialty per agent', () => {
    for (const agent of MOCK_AGENTS) {
      expect(agent.specialties.length).toBeGreaterThanOrEqual(1);
    }
  });

  it('should have ratings between 1 and 5', () => {
    for (const agent of MOCK_AGENTS) {
      expect(agent.rating).toBeGreaterThanOrEqual(1);
      expect(agent.rating).toBeLessThanOrEqual(5);
    }
  });

  it('should have non-negative propertiesCount', () => {
    for (const agent of MOCK_AGENTS) {
      expect(agent.propertiesCount).toBeGreaterThanOrEqual(0);
    }
  });
});

describe('getAgentById', () => {
  it('should return the correct agent for a known ID', () => {
    const agent = getAgentById('agent-001');
    expect(agent).toBeDefined();
    expect(agent!.name).toBe('David Mitchell');
  });

  it('should return the correct agent for agent-002', () => {
    const agent = getAgentById('agent-002');
    expect(agent).toBeDefined();
    expect(agent!.name).toBe('Sarah Chen');
  });

  it('should return the correct agent for agent-003', () => {
    const agent = getAgentById('agent-003');
    expect(agent).toBeDefined();
    expect(agent!.name).toBe('Marcus Rivera');
  });

  it('should return undefined for an unknown ID', () => {
    const agent = getAgentById('agent-999');
    expect(agent).toBeUndefined();
  });
});
