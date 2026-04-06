/**
 * Mock agent data with Unsplash portrait URLs for development.
 */

import type { Agent } from '../types/models';

/** Sample agents used throughout the application during development. */
export const MOCK_AGENTS: Agent[] = [
  {
    id: 'agent-1',
    name: 'James Mitchell',
    title: 'Senior Real Estate Broker',
    phone: '(555) 123-4567',
    email: 'james.mitchell@luxeestates.com',
    photo: 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&h=400&fit=crop',
    bio: 'James brings over 15 years of experience in luxury residential real estate. His deep knowledge of the local market and commitment to client satisfaction have earned him a reputation as one of the top agents in the region.',
    specialties: ['Luxury Homes', 'Waterfront Properties', 'Investment Properties'],
    propertiesCount: 42,
    rating: 4.9,
    socialLinks: {
      linkedin: 'https://linkedin.com/in/jamesmitchell',
      twitter: 'https://twitter.com/jamesmitchell',
    },
  },
  {
    id: 'agent-2',
    name: 'Sarah Chen',
    title: 'Residential Sales Specialist',
    phone: '(555) 234-5678',
    email: 'sarah.chen@luxeestates.com',
    photo: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop',
    bio: 'Sarah specializes in helping first-time buyers and families find their dream homes. Her patient approach and detailed market analysis make the buying process smooth and enjoyable.',
    specialties: ['First-Time Buyers', 'Family Homes', 'Condominiums'],
    propertiesCount: 35,
    rating: 4.8,
    socialLinks: {
      linkedin: 'https://linkedin.com/in/sarahchen',
      instagram: 'https://instagram.com/sarahchen_realty',
    },
  },
  {
    id: 'agent-3',
    name: 'David Rodriguez',
    title: 'Commercial & Residential Agent',
    phone: '(555) 345-6789',
    email: 'david.rodriguez@luxeestates.com',
    photo: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop',
    bio: 'David has a unique background in both commercial and residential real estate, giving his clients a comprehensive perspective on property investments and market trends.',
    specialties: ['Commercial Properties', 'New Developments', 'Market Analysis'],
    propertiesCount: 28,
    rating: 4.7,
    socialLinks: {
      linkedin: 'https://linkedin.com/in/davidrodriguez',
      facebook: 'https://facebook.com/davidrodriguezrealty',
    },
  },
  {
    id: 'agent-4',
    name: 'Emily Parker',
    title: 'Luxury Property Consultant',
    phone: '(555) 456-7890',
    email: 'emily.parker@luxeestates.com',
    photo: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400&h=400&fit=crop',
    bio: 'Emily is passionate about connecting discerning buyers with exceptional properties. Her eye for design and understanding of luxury living ensure that every client finds a home that matches their lifestyle.',
    specialties: ['Luxury Estates', 'Historic Homes', 'Relocation Services'],
    propertiesCount: 31,
    rating: 4.9,
    socialLinks: {
      linkedin: 'https://linkedin.com/in/emilyparker',
      instagram: 'https://instagram.com/emilyparker_luxury',
    },
  },
];

/**
 * Find an agent by their unique identifier.
 *
 * @param id - The agent's unique id string.
 * @returns The matching Agent or undefined if not found.
 */
export function getAgentById(id: string): Agent | undefined {
  return MOCK_AGENTS.find((agent) => agent.id === id);
}
