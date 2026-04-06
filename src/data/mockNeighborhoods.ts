import { Neighborhood } from '../types/models';

export const MOCK_NEIGHBORHOODS: Neighborhood[] = [
  {
    id: '1',
    name: 'Lake Travis',
    slug: 'lake-travis',
    city: 'Austin',
    state: 'TX',
    description: 'A premier lakeside community known for stunning waterfront homes, outdoor recreation, and a laid-back Texas lifestyle.',
    image: 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop',
    averagePrice: 1675000,
    walkScore: 45,
    transitScore: 30,
    highlights: ['Waterfront Living', 'Boating & Water Sports', 'Hill Country Views', 'Top-Rated Schools'],
    featuredProperties: ['1', '4']
  },
  {
    id: '2',
    name: 'LoDo District',
    slug: 'lodo-district',
    city: 'Denver',
    state: 'CO',
    description: 'Denver\'s vibrant lower downtown neighborhood featuring historic warehouses turned luxury lofts, world-class dining, and walkable streets.',
    image: 'https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=800&h=600&fit=crop',
    averagePrice: 580000,
    walkScore: 95,
    transitScore: 88,
    highlights: ['Walkable', 'Nightlife & Dining', 'Sports Venues', 'Art Galleries'],
    featuredProperties: ['2', '5']
  },
  {
    id: '3',
    name: 'Nob Hill',
    slug: 'nob-hill',
    city: 'Portland',
    state: 'OR',
    description: 'A charming, tree-lined neighborhood with a mix of historic homes and modern townhouses, close to parks and local boutiques.',
    image: 'https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=800&h=600&fit=crop',
    averagePrice: 525000,
    walkScore: 88,
    transitScore: 75,
    highlights: ['Tree-Lined Streets', 'Local Shops', 'Parks & Trails', 'Community Events'],
    featuredProperties: ['3']
  },
  {
    id: '4',
    name: 'Hawthorne',
    slug: 'hawthorne',
    city: 'Portland',
    state: 'OR',
    description: 'One of Portland\'s most eclectic neighborhoods, known for its indie shops, vintage stores, diverse food scene, and craftsman-style homes.',
    image: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&h=600&fit=crop',
    averagePrice: 475000,
    walkScore: 91,
    transitScore: 80,
    highlights: ['Eclectic Culture', 'Food Scene', 'Vintage Shopping', 'Bike Friendly'],
    featuredProperties: ['6']
  }
];

export function getNeighborhoodBySlug(slug: string): Neighborhood | undefined {
  return MOCK_NEIGHBORHOODS.find((n) => n.slug === slug);
}
