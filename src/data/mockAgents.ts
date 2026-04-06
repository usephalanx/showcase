/**
 * Mock agent data for development.
 *
 * Provides a static array of agent profiles and a lookup helper.
 */

import type { Agent } from "../types/models";

/** Sample real estate agents. */
export const MOCK_AGENTS: Agent[] = [
  {
    id: "agent-1",
    name: "James Mitchell",
    title: "Senior Real Estate Agent",
    phone: "(555) 123-4567",
    email: "james.mitchell@realestate.com",
    photo:
      "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&h=400&fit=crop",
    bio: "With over 15 years of experience in luxury residential real estate, James has helped hundreds of families find their dream homes. He specializes in waterfront properties and historic estates.",
    specialties: ["Luxury Homes", "Waterfront Properties", "Historic Estates"],
    propertiesCount: 24,
    rating: 4.9,
    socialLinks: {
      linkedin: "https://linkedin.com/in/jamesmitchell",
      twitter: "https://twitter.com/jamesmitchell",
    },
  },
  {
    id: "agent-2",
    name: "Sarah Chen",
    title: "Buyer's Specialist",
    phone: "(555) 234-5678",
    email: "sarah.chen@realestate.com",
    photo:
      "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop",
    bio: "Sarah is passionate about helping first-time buyers navigate the market with confidence. Her deep knowledge of urban condos and townhouses makes her an invaluable resource.",
    specialties: ["First-Time Buyers", "Condos", "Townhouses"],
    propertiesCount: 18,
    rating: 4.8,
    socialLinks: {
      linkedin: "https://linkedin.com/in/sarahchen",
      instagram: "https://instagram.com/sarahchenrealty",
    },
  },
  {
    id: "agent-3",
    name: "Michael Torres",
    title: "Commercial & Residential Agent",
    phone: "(555) 345-6789",
    email: "michael.torres@realestate.com",
    photo:
      "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop",
    bio: "Michael brings a unique dual expertise in both commercial and residential markets. His analytical approach and strong negotiation skills consistently deliver exceptional results for his clients.",
    specialties: ["Commercial Properties", "Investment Properties", "Negotiation"],
    propertiesCount: 31,
    rating: 4.7,
    socialLinks: {
      linkedin: "https://linkedin.com/in/michaeltorres",
      facebook: "https://facebook.com/michaeltorresrealty",
    },
  },
  {
    id: "agent-4",
    name: "Emily Rodriguez",
    title: "Luxury Property Specialist",
    phone: "(555) 456-7890",
    email: "emily.rodriguez@realestate.com",
    photo:
      "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400&h=400&fit=crop",
    bio: "Emily's eye for design and deep connections in the luxury market set her apart. She works closely with architects and designers to stage and present properties at their absolute best.",
    specialties: ["Luxury Homes", "Interior Staging", "New Construction"],
    propertiesCount: 15,
    rating: 5.0,
    socialLinks: {
      linkedin: "https://linkedin.com/in/emilyrodriguez",
      instagram: "https://instagram.com/emilyrodriguezluxury",
    },
  },
];

/**
 * Look up a single agent by their unique identifier.
 *
 * @param id - The agent ID to search for.
 * @returns The matching Agent, or undefined if not found.
 */
export function getAgentById(id: string): Agent | undefined {
  return MOCK_AGENTS.find((agent) => agent.id === id);
}
