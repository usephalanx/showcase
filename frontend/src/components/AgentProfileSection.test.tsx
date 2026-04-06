import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import AgentProfileSection, { Agent } from './AgentProfileSection';

const mockAgents: Agent[] = [
  {
    id: '1',
    name: 'Sarah Johnson',
    title: 'Senior Real Estate Agent',
    phone: '(555) 123-4567',
    email: 'sarah@example.com',
    photo: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop',
    bio: 'Sarah has over 15 years of experience in residential real estate, specializing in luxury homes and waterfront properties.',
    specialties: ['Luxury Homes', 'Waterfront'],
    propertiesCount: 42,
    rating: 4.9,
    socialLinks: {
      linkedin: 'https://linkedin.com/in/sarah',
      twitter: 'https://twitter.com/sarah',
    },
  },
  {
    id: '2',
    name: 'Michael Chen',
    title: 'Buyer Specialist',
    phone: '(555) 234-5678',
    email: 'michael@example.com',
    photo: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop',
    bio: 'Michael is passionate about helping first-time buyers navigate the market with confidence.',
    specialties: ['First-Time Buyers', 'Condos'],
    propertiesCount: 28,
    rating: 4.7,
  },
  {
    id: '3',
    name: 'Emily Rodriguez',
    title: 'Listing Agent',
    phone: '(555) 345-6789',
    email: 'emily@example.com',
    photo: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400&h=400&fit=crop',
    bio: 'Emily consistently achieves above-asking-price sales with her innovative marketing strategies.',
    specialties: ['Marketing', 'Staging'],
    propertiesCount: 35,
    rating: 4.8,
  },
];

describe('AgentProfileSection', () => {
  it('renders without crashing', () => {
    render(<AgentProfileSection agents={mockAgents} />);
    expect(screen.getByTestId('agent-profile-section')).toBeInTheDocument();
  });

  it('renders the default heading', () => {
    render(<AgentProfileSection agents={mockAgents} />);
    expect(screen.getByText('Meet Our Agents')).toBeInTheDocument();
  });

  it('renders a custom heading when provided', () => {
    render(<AgentProfileSection agents={mockAgents} heading="Our Team" />);
    expect(screen.getByText('Our Team')).toBeInTheDocument();
    expect(screen.queryByText('Meet Our Agents')).not.toBeInTheDocument();
  });

  it('renders the default intro paragraph', () => {
    render(<AgentProfileSection agents={mockAgents} />);
    expect(
      screen.getByText(/Our team of experienced real estate professionals/)
    ).toBeInTheDocument();
  });

  it('renders a custom intro paragraph when provided', () => {
    const customIntro = 'Custom intro text for the section.';
    render(<AgentProfileSection agents={mockAgents} introParagraph={customIntro} />);
    expect(screen.getByText(customIntro)).toBeInTheDocument();
  });

  it('renders all agent cards', () => {
    render(<AgentProfileSection agents={mockAgents} />);
    expect(screen.getByTestId('agent-card-1')).toBeInTheDocument();
    expect(screen.getByTestId('agent-card-2')).toBeInTheDocument();
    expect(screen.getByTestId('agent-card-3')).toBeInTheDocument();
  });

  it('displays agent names', () => {
    render(<AgentProfileSection agents={mockAgents} />);
    expect(screen.getByText('Sarah Johnson')).toBeInTheDocument();
    expect(screen.getByText('Michael Chen')).toBeInTheDocument();
    expect(screen.getByText('Emily Rodriguez')).toBeInTheDocument();
  });

  it('displays agent titles', () => {
    render(<AgentProfileSection agents={mockAgents} />);
    expect(screen.getByText('Senior Real Estate Agent')).toBeInTheDocument();
    expect(screen.getByText('Buyer Specialist')).toBeInTheDocument();
    expect(screen.getByText('Listing Agent')).toBeInTheDocument();
  });

  it('displays agent bios', () => {
    render(<AgentProfileSection agents={mockAgents} />);
    expect(screen.getByText(/Sarah has over 15 years/)).toBeInTheDocument();
    expect(screen.getByText(/Michael is passionate/)).toBeInTheDocument();
  });

  it('displays agent specialties', () => {
    render(<AgentProfileSection agents={mockAgents} />);
    expect(screen.getByText('Luxury Homes')).toBeInTheDocument();
    expect(screen.getByText('Waterfront')).toBeInTheDocument();
    expect(screen.getByText('First-Time Buyers')).toBeInTheDocument();
    expect(screen.getByText('Condos')).toBeInTheDocument();
  });

  it('displays agent emails as links', () => {
    render(<AgentProfileSection agents={mockAgents} />);
    const sarahEmail = screen.getByText('sarah@example.com');
    expect(sarahEmail).toBeInTheDocument();
    expect(sarahEmail.closest('a')).toHaveAttribute('href', 'mailto:sarah@example.com');
  });

  it('displays agent phone numbers as links', () => {
    render(<AgentProfileSection agents={mockAgents} />);
    const sarahPhone = screen.getByText('(555) 123-4567');
    expect(sarahPhone).toBeInTheDocument();
    expect(sarahPhone.closest('a')).toHaveAttribute('href', 'tel:(555) 123-4567');
  });

  it('displays properties count for each agent', () => {
    render(<AgentProfileSection agents={mockAgents} />);
    expect(screen.getByText('42')).toBeInTheDocument();
    expect(screen.getByText('28')).toBeInTheDocument();
    expect(screen.getByText('35')).toBeInTheDocument();
  });

  it('renders agent photos with correct alt text', () => {
    render(<AgentProfileSection agents={mockAgents} />);
    const sarahImg = screen.getByAlt('Sarah Johnson') as HTMLImageElement;
    expect(sarahImg).toBeInTheDocument();
    expect(sarahImg.src).toContain('unsplash');
  });

  it('displays rating information', () => {
    render(<AgentProfileSection agents={mockAgents} />);
    expect(screen.getByText('(4.9)')).toBeInTheDocument();
    expect(screen.getByText('(4.7)')).toBeInTheDocument();
    expect(screen.getByText('(4.8)')).toBeInTheDocument();
  });

  it('shows a message when agents array is empty', () => {
    render(<AgentProfileSection agents={[]} />);
    expect(screen.getByTestId('no-agents-message')).toBeInTheDocument();
    expect(screen.getByText('No agents available at this time.')).toBeInTheDocument();
  });

  it('renders social links when provided', () => {
    render(<AgentProfileSection agents={mockAgents} />);
    const linkedinLink = screen.getByLabelText('Sarah Johnson LinkedIn');
    expect(linkedinLink).toHaveAttribute('href', 'https://linkedin.com/in/sarah');
    expect(linkedinLink).toHaveAttribute('target', '_blank');
    expect(linkedinLink).toHaveAttribute('rel', 'noopener noreferrer');
  });

  it('renders with a single agent', () => {
    render(<AgentProfileSection agents={[mockAgents[0]]} />);
    expect(screen.getByTestId('agent-card-1')).toBeInTheDocument();
    expect(screen.queryByTestId('agent-card-2')).not.toBeInTheDocument();
  });
});
