import { Agent } from '../types/models';

export const MOCK_AGENTS: Agent[] = [
  {
    id: 'agent-1',
    name: 'Sarah Johnson',
    title: 'Senior Real Estate Agent',
    phone: '(555) 123-4567',
    email: 'sarah.johnson@realty.com',
    photo: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop',
    bio: 'With over 15 years of experience in luxury real estate, Sarah has helped hundreds of families find their dream homes. She specializes in waterfront properties and historic estates.',
    specialties: ['Luxury Homes', 'Waterfront Properties', 'Historic Estates'],
    propertiesCount: 42,
    rating: 4.9,
    socialLinks: { linkedin: '#', twitter: '#' },
  },
  {
    id: 'agent-2',
    name: 'Michael Chen',
    title: 'Broker Associate',
    phone: '(555) 234-5678',
    email: 'michael.chen@realty.com',
    photo: 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&h=400&fit=crop',
    bio: 'Michael brings a data-driven approach to real estate, helping clients make informed decisions. His background in finance gives him a unique edge in negotiations.',
    specialties: ['Investment Properties', 'Condos', 'New Construction'],
    propertiesCount: 38,
    rating: 4.8,
    socialLinks: { linkedin: '#' },
  },
  {
    id: 'agent-3',
    name: 'Emily Rodriguez',
    title: 'Real Estate Agent',
    phone: '(555) 345-6789',
    email: 'emily.rodriguez@realty.com',
    photo: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400&h=400&fit=crop',
    bio: 'Emily is passionate about helping first-time homebuyers navigate the market. Her patient and thorough approach ensures every client feels confident in their purchase.',
    specialties: ['First-Time Buyers', 'Townhouses', 'Suburban Homes'],
    propertiesCount: 27,
    rating: 4.9,
    socialLinks: { linkedin: '#', facebook: '#' },
  },
  {
    id: 'agent-4',
    name: 'David Park',
    title: 'Luxury Property Specialist',
    phone: '(555) 456-7890',
    email: 'david.park@realty.com',
    photo: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop',
    bio: 'David has been recognized as a top producer for five consecutive years. He specializes in high-end properties and provides white-glove service to all his clients.',
    specialties: ['Luxury Homes', 'Penthouses', 'Estate Properties'],
    propertiesCount: 53,
    rating: 5.0,
    socialLinks: { linkedin: '#', twitter: '#', facebook: '#' },
  },
];

export function getAgentById(id: string): Agent | undefined {
  return MOCK_AGENTS.find((a) => a.id === id);
}
