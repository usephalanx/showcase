import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import NeighborhoodHighlights, {
  NeighborhoodData,
  NeighborhoodHighlightsProps,
} from './NeighborhoodHighlights';

const mockNeighborhoods: NeighborhoodData[] = [
  {
    id: '1',
    name: 'Beverly Hills',
    slug: 'beverly-hills',
    city: 'Los Angeles',
    state: 'CA',
    description: 'Iconic luxury neighborhood known for world-class shopping and stunning estates.',
    image: 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop',
    averagePrice: 3500000,
    walkScore: 86,
    transitScore: 62,
    highlights: ['Fine Dining', 'Designer Shops', 'Celebrity Estates'],
  },
  {
    id: '2',
    name: 'Manhattan Beach',
    slug: 'manhattan-beach',
    city: 'Los Angeles',
    state: 'CA',
    description: 'A coastal gem with pristine beaches and a vibrant downtown scene.',
    image: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&h=600&fit=crop',
    averagePrice: 2800000,
    walkScore: 74,
    transitScore: 45,
    highlights: ['Beachfront', 'Top Schools', 'Pier Walk'],
  },
  {
    id: '3',
    name: 'Bel Air',
    slug: 'bel-air',
    city: 'Los Angeles',
    state: 'CA',
    description: 'Ultra-exclusive gated community with sprawling estates and panoramic views.',
    image: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&h=600&fit=crop',
    averagePrice: 5200000,
    walkScore: 32,
    transitScore: 18,
    highlights: ['Gated Community', 'Mountain Views', 'Private Estates'],
  },
];

describe('NeighborhoodHighlights', () => {
  it('renders without crashing', () => {
    render(<NeighborhoodHighlights neighborhoods={[]} />);
    expect(screen.getByTestId('neighborhood-highlights')).toBeInTheDocument();
  });

  it('displays the default heading', () => {
    render(<NeighborhoodHighlights neighborhoods={[]} />);
    expect(screen.getByTestId('section-heading')).toHaveTextContent('Explore Neighborhoods');
  });

  it('displays a custom heading when provided', () => {
    render(
      <NeighborhoodHighlights
        neighborhoods={[]}
        heading="Top Neighborhoods"
      />
    );
    expect(screen.getByTestId('section-heading')).toHaveTextContent('Top Neighborhoods');
  });

  it('displays the subheading when provided', () => {
    render(
      <NeighborhoodHighlights
        neighborhoods={[]}
        subheading="Discover the best places to live"
      />
    );
    expect(screen.getByTestId('section-subheading')).toHaveTextContent(
      'Discover the best places to live'
    );
  });

  it('does not render subheading when not provided', () => {
    render(<NeighborhoodHighlights neighborhoods={[]} />);
    expect(screen.queryByTestId('section-subheading')).not.toBeInTheDocument();
  });

  it('renders all neighborhood cards', () => {
    render(<NeighborhoodHighlights neighborhoods={mockNeighborhoods} />);
    expect(screen.getByTestId('neighborhood-card-1')).toBeInTheDocument();
    expect(screen.getByTestId('neighborhood-card-2')).toBeInTheDocument();
    expect(screen.getByTestId('neighborhood-card-3')).toBeInTheDocument();
  });

  it('displays neighborhood names', () => {
    render(<NeighborhoodHighlights neighborhoods={mockNeighborhoods} />);
    expect(screen.getByText('Beverly Hills')).toBeInTheDocument();
    expect(screen.getByText('Manhattan Beach')).toBeInTheDocument();
    expect(screen.getByText('Bel Air')).toBeInTheDocument();
  });

  it('displays city and state for each neighborhood', () => {
    render(<NeighborhoodHighlights neighborhoods={mockNeighborhoods} />);
    const cityStateElements = screen.getAllByText('Los Angeles, CA');
    expect(cityStateElements.length).toBe(3);
  });

  it('displays neighborhood descriptions', () => {
    render(<NeighborhoodHighlights neighborhoods={mockNeighborhoods} />);
    expect(
      screen.getByText(/Iconic luxury neighborhood known for world-class/)
    ).toBeInTheDocument();
  });

  it('displays formatted average prices', () => {
    render(<NeighborhoodHighlights neighborhoods={mockNeighborhoods} />);
    expect(screen.getByText('$3.5M')).toBeInTheDocument();
    expect(screen.getByText('$2.8M')).toBeInTheDocument();
    expect(screen.getByText('$5.2M')).toBeInTheDocument();
  });

  it('displays walk scores and transit scores', () => {
    render(<NeighborhoodHighlights neighborhoods={mockNeighborhoods} />);
    expect(screen.getByText('86')).toBeInTheDocument();
    expect(screen.getByText('62')).toBeInTheDocument();
  });

  it('displays highlight tags', () => {
    render(<NeighborhoodHighlights neighborhoods={mockNeighborhoods} />);
    expect(screen.getByText('Fine Dining')).toBeInTheDocument();
    expect(screen.getByText('Designer Shops')).toBeInTheDocument();
    expect(screen.getByText('Celebrity Estates')).toBeInTheDocument();
    expect(screen.getByText('Beachfront')).toBeInTheDocument();
  });

  it('limits highlights to 3 per card', () => {
    const neighborhoodWithManyHighlights: NeighborhoodData[] = [
      {
        ...mockNeighborhoods[0],
        highlights: ['A', 'B', 'C', 'D', 'E'],
      },
    ];
    render(
      <NeighborhoodHighlights neighborhoods={neighborhoodWithManyHighlights} />
    );
    expect(screen.getByText('A')).toBeInTheDocument();
    expect(screen.getByText('B')).toBeInTheDocument();
    expect(screen.getByText('C')).toBeInTheDocument();
    expect(screen.queryByText('D')).not.toBeInTheDocument();
    expect(screen.queryByText('E')).not.toBeInTheDocument();
  });

  it('renders images with correct alt text', () => {
    render(<NeighborhoodHighlights neighborhoods={mockNeighborhoods} />);
    const img = screen.getByAlt('Beverly Hills neighborhood');
    expect(img).toBeInTheDocument();
    expect(img).toHaveAttribute('src', mockNeighborhoods[0].image);
  });

  it('shows empty state when no neighborhoods are provided', () => {
    render(<NeighborhoodHighlights neighborhoods={[]} />);
    expect(screen.getByTestId('empty-state')).toHaveTextContent(
      'No neighborhoods to display.'
    );
  });

  it('does not show empty state when neighborhoods are present', () => {
    render(<NeighborhoodHighlights neighborhoods={mockNeighborhoods} />);
    expect(screen.queryByTestId('empty-state')).not.toBeInTheDocument();
  });

  it('calls onNeighborhoodClick when a card is clicked', () => {
    const handleClick = vi.fn();
    render(
      <NeighborhoodHighlights
        neighborhoods={mockNeighborhoods}
        onNeighborhoodClick={handleClick}
      />
    );
    fireEvent.click(screen.getByTestId('neighborhood-card-1'));
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith(mockNeighborhoods[0]);
  });

  it('calls onNeighborhoodClick on Enter key press', () => {
    const handleClick = vi.fn();
    render(
      <NeighborhoodHighlights
        neighborhoods={mockNeighborhoods}
        onNeighborhoodClick={handleClick}
      />
    );
    fireEvent.keyDown(screen.getByTestId('neighborhood-card-2'), {
      key: 'Enter',
    });
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith(mockNeighborhoods[1]);
  });

  it('calls onNeighborhoodClick on Space key press', () => {
    const handleClick = vi.fn();
    render(
      <NeighborhoodHighlights
        neighborhoods={mockNeighborhoods}
        onNeighborhoodClick={handleClick}
      />
    );
    fireEvent.keyDown(screen.getByTestId('neighborhood-card-3'), {
      key: ' ',
    });
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith(mockNeighborhoods[2]);
  });

  it('does not crash when onNeighborhoodClick is not provided', () => {
    render(<NeighborhoodHighlights neighborhoods={mockNeighborhoods} />);
    expect(() => {
      fireEvent.click(screen.getByTestId('neighborhood-card-1'));
    }).not.toThrow();
  });

  it('renders the grid container', () => {
    render(<NeighborhoodHighlights neighborhoods={mockNeighborhoods} />);
    const grid = screen.getByTestId('neighborhood-grid');
    expect(grid).toBeInTheDocument();
    expect(grid.children.length).toBe(3);
  });

  it('handles neighborhoods with empty highlights array', () => {
    const noHighlights: NeighborhoodData[] = [
      {
        ...mockNeighborhoods[0],
        highlights: [],
      },
    ];
    render(<NeighborhoodHighlights neighborhoods={noHighlights} />);
    expect(screen.getByTestId('neighborhood-card-1')).toBeInTheDocument();
  });

  it('formats prices under 1M correctly', () => {
    const cheapNeighborhood: NeighborhoodData[] = [
      {
        ...mockNeighborhoods[0],
        averagePrice: 750000,
      },
    ];
    render(<NeighborhoodHighlights neighborhoods={cheapNeighborhood} />);
    expect(screen.getByText('$750K')).toBeInTheDocument();
  });
});
