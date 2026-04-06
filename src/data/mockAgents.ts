/**
 * Mock agent data for development and testing.
 *
 * Provides a static array of Agent objects and a helper function to
 * retrieve an agent by ID.
 */

import type { Agent } from "../types/models";

/** Static list of mock agents. */
export const MOCK_AGENTS: Agent[] = [
  {
    id: "agent-1",
    name: "James Mitchell",
    title: "Senior Real Estate Agent",
    phone: "(555) 100-2001",
    email: "james.mitchell@realestate.example",
    photo:
      "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&h=400&fit=crop",
    bio: "James has over 15 years of experience in luxury residential sales. Known for his deep market knowledge and hands-on approach, he has helped hundreds of families find their perfect home.",
    specialties: ["Luxury Homes", "Waterfront Properties", "Investment"],
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
    title: "Lead Listing Agent",
    phone: "(555) 100-2002",
    email: "sarah.chen@realestate.example",
    photo:
      "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop",
    bio: "Sarah specializes in urban condos and townhouses. Her marketing strategies consistently result in above-asking-price sales and record-breaking close times.",
    specialties: ["Condos", "Townhouses", "First-Time Buyers"],
    propertiesCount: 18,
    rating: 4.8,
    socialLinks: {
      linkedin: "https://linkedin.com/in/sarachen",
      instagram: "https://instagram.com/sarachen_realty",
    },
  },
  {
    id: "agent-3",
    name: "Michael Rivera",
    title: "Buyer's Agent",
    phone: "(555) 100-2003",
    email: "michael.rivera@realestate.example",
    photo:
      "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop",
    bio: "Michael is passionate about helping buyers navigate the competitive market. With a background in finance, he offers unparalleled insight into property valuations and negotiation.",
    specialties: ["Buyer Representation", "Relocation", "Negotiation"],
    propertiesCount: 12,
    rating: 4.7,
    socialLinks: {
      linkedin: "https://linkedin.com/in/michaelrivera",
      facebook: "https://facebook.com/michaelrivera.realty",
    },
  },
  {
    id: "agent-4",
    name: "Emily Nakamura",
    title: "Luxury Property Specialist",
    phone: "(555) 100-2004",
    email: "emily.nakamura@realestate.example",
    photo:
      "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400&h=400&fit=crop",
    bio: "Emily brings a refined eye for design and architecture to every transaction. Her clientele includes high-net-worth individuals seeking distinctive homes with character.",
    specialties: ["Luxury Homes", "Historic Properties", "Architecture"],
    propertiesCount: 15,
    rating: 4.9,
    socialLinks: {
      linkedin: "https://linkedin.com/in/emilynakamura",
      instagram: "https://instagram.com/emily_luxhomes",
    },
  },
];

/**
 * Retrieve a single agent by their unique ID.
 *
 * @param id - The agent ID to look up.
 * @returns The matching Agent object, or undefined if not found.
 */
export function getAgentById(id: string): Agent | undefined {
  return MOCK_AGENTS.find((agent) => agent.id === id);
}
