import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import AgentCard from './AgentCard';
import type { Agent } from '../types/models';

const mockAgent: Agent = {
  id: 'agent-1',
  name: 'Jane Doe',
  title: 'Senior Real Estate Agent',
  phone: '(555) 123-4567',
  email: 'jane.doe@realty.com',
  photo: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop',
  bio: 'With over 15 years of experience in luxury real estate, Jane specializes in helping families find their dream homes in the greater metropolitan area.',
  specialties: ['Luxury Homes', 'Waterfront Properties'],
  propertiesCount: 42,
  rating: 4.9,
  socialLinks: {
    linkedin: 'https://linkedin.com/in/janedoe',
  },
};

describe('AgentCard', () => {
  it('renders without crashing', () => {
    const onContact = vi.fn();
    render(<AgentCard agent={mockAgent} onContact={onContact} />);
    expect(screen.getByTestId('agent-card')).toBeInTheDocument();
  });

  it('displays the agent name', () => {
    render(<AgentCard agent={mockAgent} onContact={vi.fn()} />);
    expect(screen.getByText('Jane Doe')).toBeInTheDocument();
  });

  it('displays the agent title', () => {
    render(<AgentCard agent={mockAgent} onContact={vi.fn()} />);
    expect(screen.getByText('Senior Real Estate Agent')).toBeInTheDocument();
  });

  it('displays the agent phone number', () => {
    render(<AgentCard agent={mockAgent} onContact={vi.fn()} />);
    const phoneLinks = screen.getAllByTestId('agent-phone');
    expect(phoneLinks.length).toBeGreaterThan(0);
    expect(phoneLinks[0]).toHaveTextContent('(555) 123-4567');
  });

  it('displays the agent email', () => {
    render(<AgentCard agent={mockAgent} onContact={vi.fn()} />);
    const emailLinks = screen.getAllByTestId('agent-email');
    expect(emailLinks.length).toBeGreaterThan(0);
    expect(emailLinks[0]).toHaveTextContent('jane.doe@realty.com');
  });

  it('displays the agent bio', () => {
    render(<AgentCard agent={mockAgent} onContact={vi.fn()} />);
    expect(screen.getByText(/With over 15 years/)).toBeInTheDocument();
  });

  it('renders the agent headshot with correct src and alt', () => {
    render(<AgentCard agent={mockAgent} onContact={vi.fn()} />);
    const img = screen.getByAlt('Jane Doe headshot') as HTMLImageElement;
    expect(img).toBeInTheDocument();
    expect(img.src).toBe(mockAgent.photo);
  });

  it('calls onContact with the agent when button is clicked', () => {
    const onContact = vi.fn();
    render(<AgentCard agent={mockAgent} onContact={onContact} />);
    fireEvent.click(screen.getByTestId('contact-button'));
    expect(onContact).toHaveBeenCalledTimes(1);
    expect(onContact).toHaveBeenCalledWith(mockAgent);
  });

  it('renders the Contact Agent button text', () => {
    render(<AgentCard agent={mockAgent} onContact={vi.fn()} />);
    expect(screen.getByTestId('contact-button')).toHaveTextContent('Contact Agent');
  });

  it('renders in vertical layout by default', () => {
    render(<AgentCard agent={mockAgent} onContact={vi.fn()} />);
    const card = screen.getByTestId('agent-card');
    expect(card.className).toContain('text-center');
  });

  it('renders in horizontal layout when specified', () => {
    render(<AgentCard agent={mockAgent} onContact={vi.fn()} layout="horizontal" />);
    const card = screen.getByTestId('agent-card');
    expect(card.className).toContain('flex-row');
    expect(card.className).not.toContain('text-center');
  });

  it('applies custom className', () => {
    render(
      <AgentCard agent={mockAgent} onContact={vi.fn()} className="my-custom-class" />
    );
    const card = screen.getByTestId('agent-card');
    expect(card.className).toContain('my-custom-class');
  });

  it('renders phone link with tel: href', () => {
    render(<AgentCard agent={mockAgent} onContact={vi.fn()} />);
    const phoneLinks = screen.getAllByTestId('agent-phone');
    expect(phoneLinks[0].closest('a')).toHaveAttribute('href', 'tel:(555) 123-4567');
  });

  it('renders email link with mailto: href', () => {
    render(<AgentCard agent={mockAgent} onContact={vi.fn()} />);
    const emailLinks = screen.getAllByTestId('agent-email');
    expect(emailLinks[0].closest('a')).toHaveAttribute('href', 'mailto:jane.doe@realty.com');
  });

  it('renders correctly with a different agent', () => {
    const otherAgent: Agent = {
      ...mockAgent,
      id: 'agent-2',
      name: 'John Smith',
      title: 'Broker Associate',
      phone: '(555) 987-6543',
      email: 'john.smith@realty.com',
      bio: 'John brings a decade of market expertise.',
    };
    render(<AgentCard agent={otherAgent} onContact={vi.fn()} />);
    expect(screen.getByText('John Smith')).toBeInTheDocument();
    expect(screen.getByText('Broker Associate')).toBeInTheDocument();
    expect(screen.getByText(/John brings a decade/)).toBeInTheDocument();
  });
});
