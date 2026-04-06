/**
 * Mock real estate agent data for development and testing.
 *
 * Contains 3 agent profiles with real Unsplash portrait photo IDs.
 */

import type { Agent } from '../types/models';

export const MOCK_AGENTS: Agent[] = [
  {
    id: 'agent-001',
    name: 'David Mitchell',
    title: 'Senior Listing Agent',
    phone: '(512) 555-0142',
    email: 'david.mitchell@premierhomes.com',
    photo:
      'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&h=400&fit=crop',
    bio: 'With over 15 years of experience in the Austin luxury market, David has closed more than $200 million in residential transactions. His deep knowledge of Hill Country estates and lakefront properties makes him the go-to advisor for discerning buyers. A University of Texas alumnus and avid sailor, David brings the same precision and calm focus to every deal.',
    specialties: [
      'Luxury homes',
      'Lakefront properties',
      'Hill Country estates',
      'Investment properties',
    ],
    propertiesCount: 24,
    rating: 4.9,
    socialLinks: {
      linkedin: 'https://linkedin.com/in/david-mitchell',
      instagram: 'https://instagram.com/davidmitchell_realty',
    },
  },
  {
    id: 'agent-002',
    name: 'Sarah Chen',
    title: 'Buyer Specialist & Relocation Expert',
    phone: '(512) 555-0287',
    email: 'sarah.chen@premierhomes.com',
    photo:
      'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop',
    bio: 'Sarah specializes in helping families and tech professionals relocate to Austin. Fluent in Mandarin and English, she's guided over 300 families to their dream homes. Her data-driven approach, neighborhood expertise, and patient negotiating style consistently earn five-star reviews. Outside of real estate Sarah is a marathon runner and volunteer CASA advocate.',
    specialties: [
      'Buyer representation',
      'Relocation services',
      'Condos & townhomes',
      'First-time buyers',
    ],
    propertiesCount: 18,
    rating: 4.8,
    socialLinks: {
      linkedin: 'https://linkedin.com/in/sarah-chen-realtor',
      twitter: 'https://twitter.com/sarahchen_atx',
      facebook: 'https://facebook.com/sarahchenrealty',
    },
  },
  {
    id: 'agent-003',
    name: 'Marcus Rivera',
    title: 'Neighborhood Specialist & Listing Agent',
    phone: '(512) 555-0319',
    email: 'marcus.rivera@premierhomes.com',
    photo:
      'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop',
    bio: 'Born and raised in South Austin, Marcus has an unrivaled understanding of the city's diverse neighborhoods. From historic Travis Heights to the booming Riverside corridor, he provides hyper-local insight that only a lifelong resident can offer. A licensed contractor before entering real estate, Marcus brings a unique eye for renovation potential and construction quality.',
    specialties: [
      'South Austin neighborhoods',
      'Historic homes',
      'Renovation potential',
      'Investment analysis',
    ],
    propertiesCount: 15,
    rating: 4.7,
    socialLinks: {
      linkedin: 'https://linkedin.com/in/marcus-rivera-atx',
      instagram: 'https://instagram.com/marcusrivera_homes',
    },
  },
];

/**
 * Look up a single agent by their unique ID.
 *
 * @param id - The agent ID to search for.
 * @returns The matching Agent or undefined.
 */
export function getAgentById(id: string): Agent | undefined {
  return MOCK_AGENTS.find((agent) => agent.id === id);
}
