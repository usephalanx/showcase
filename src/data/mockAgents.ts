import { Agent } from '../types/models';

export const MOCK_AGENTS: Agent[] = [
  {
    id: '1',
    name: 'James Mitchell',
    title: 'Senior Luxury Agent',
    phone: '(512) 555-0101',
    email: 'james@premierealty.com',
    photo: 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&h=400&fit=crop',
    bio: 'With over 15 years of experience in luxury real estate, James specializes in waterfront properties and high-end estates in the Austin area.',
    specialties: ['Luxury Homes', 'Waterfront', 'Investment Properties'],
    propertiesCount: 42,
    rating: 4.9,
    socialLinks: { linkedin: '#', twitter: '#' }
  },
  {
    id: '2',
    name: 'Sarah Chen',
    title: 'Urban Living Specialist',
    phone: '(303) 555-0202',
    email: 'sarah@premierealty.com',
    photo: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop',
    bio: 'Sarah helps clients find their perfect urban home. Her deep knowledge of Denver\'s downtown market is unmatched.',
    specialties: ['Condos', 'Downtown Living', 'First-Time Buyers'],
    propertiesCount: 38,
    rating: 4.8,
    socialLinks: { linkedin: '#', instagram: '#' }
  },
  {
    id: '3',
    name: 'Michael Torres',
    title: 'Neighborhood Expert',
    phone: '(503) 555-0303',
    email: 'michael@premierealty.com',
    photo: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop',
    bio: 'Born and raised in Portland, Michael brings unparalleled local knowledge to every transaction.',
    specialties: ['Historic Homes', 'Family Neighborhoods', 'Relocation'],
    propertiesCount: 55,
    rating: 4.7,
    socialLinks: { linkedin: '#', twitter: '#', instagram: '#' }
  },
  {
    id: '4',
    name: 'Emily Rodriguez',
    title: 'Investment Advisor',
    phone: '(303) 555-0404',
    email: 'emily@premierealty.com',
    photo: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400&h=400&fit=crop',
    bio: 'Emily combines her finance background with real estate expertise to help investors maximize returns.',
    specialties: ['Investment Properties', 'Multi-Family', 'Market Analysis'],
    propertiesCount: 29,
    rating: 4.9,
    socialLinks: { linkedin: '#' }
  }
];

export function getAgentById(id: string): Agent | undefined {
  return MOCK_AGENTS.find((a) => a.id === id);
}
