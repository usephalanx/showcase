import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import NeighborhoodCard from './NeighborhoodCard';
import type { Neighborhood } from '../types/models';

const mockNeighborhood: Neighborhood = {
  id: 'nb-1',
  name: 'Downtown Arts District',
  slug: 'downtown-arts-district',
  city: 'Austin',
  state: 'TX',
  description: 'A vibrant neighborhood full of galleries and restaurants.',
  image:
    'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop',
  averagePrice: 525000,
  propertyCount: 42,
  walkScore: 92,
  transitScore: 78,
  highlights: ['Art Galleries', 'Fine Dining', 'Nightlife'],
};

describe('NeighborhoodCard', () => {
  it('renders without crashing', () => {
    render(<NeighborhoodCard neighborhood={mockNeighborhood} />);
    expect(screen.getByTestId('neighborhood-card')).toBeTruthy();
  });

  it('displays the neighborhood name', () => {
    render(<NeighborhoodCard neighborhood={mockNeighborhood} />);
    expect(screen.getByTestId('neighborhood-card-name')).toHaveTextContent(
      'Downtown Arts District'
    );
  });

  it('displays the city and state', () => {
    render(<NeighborhoodCard neighborhood={mockNeighborhood} />);
    expect(screen.getByTestId('neighborhood-card-location')).toHaveTextContent(
      'Austin, TX'
    );
  });

  it('displays the formatted average price', () => {
    render(<NeighborhoodCard neighborhood={mockNeighborhood} />);
    expect(screen.getByTestId('neighborhood-card-price')).toHaveTextContent(
      'Avg. $525K'
    );
  });

  it('formats price in millions correctly', () => {
    const expensiveNeighborhood: Neighborhood = {
      ...mockNeighborhood,
      averagePrice: 1_500_000,
    };
    render(<NeighborhoodCard neighborhood={expensiveNeighborhood} />);
    expect(screen.getByTestId('neighborhood-card-price')).toHaveTextContent(
      'Avg. $1.5M'
    );
  });

  it('formats exact million price without decimal', () => {
    const millionNeighborhood: Neighborhood = {
      ...mockNeighborhood,
      averagePrice: 2_000_000,
    };
    render(<NeighborhoodCard neighborhood={millionNeighborhood} />);
    expect(screen.getByTestId('neighborhood-card-price')).toHaveTextContent(
      'Avg. $2M'
    );
  });

  it('displays the property count with correct pluralization', () => {
    render(<NeighborhoodCard neighborhood={mockNeighborhood} />);
    expect(screen.getByTestId('neighborhood-card-count')).toHaveTextContent(
      '42 Properties'
    );
  });

  it('uses singular "Property" for count of 1', () => {
    const singlePropertyNeighborhood: Neighborhood = {
      ...mockNeighborhood,
      propertyCount: 1,
    };
    render(
      <NeighborhoodCard neighborhood={singlePropertyNeighborhood} />
    );
    expect(screen.getByTestId('neighborhood-card-count')).toHaveTextContent(
      '1 Property'
    );
  });

  it('sets the background image from the neighborhood image prop', () => {
    render(<NeighborhoodCard neighborhood={mockNeighborhood} />);
    const imageDiv = screen.getByTestId('neighborhood-card-image');
    expect(imageDiv.style.backgroundImage).toBe(
      `url(${mockNeighborhood.image})`
    );
  });

  it('calls onClick with the neighborhood when clicked', async () => {
    const handleClick = vi.fn();
    render(
      <NeighborhoodCard
        neighborhood={mockNeighborhood}
        onClick={handleClick}
      />
    );

    await userEvent.click(screen.getByTestId('neighborhood-card'));
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith(mockNeighborhood);
  });

  it('calls onClick when Enter key is pressed', () => {
    const handleClick = vi.fn();
    render(
      <NeighborhoodCard
        neighborhood={mockNeighborhood}
        onClick={handleClick}
      />
    );

    const card = screen.getByTestId('neighborhood-card');
    fireEvent.keyDown(card, { key: 'Enter' });
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith(mockNeighborhood);
  });

  it('calls onClick when Space key is pressed', () => {
    const handleClick = vi.fn();
    render(
      <NeighborhoodCard
        neighborhood={mockNeighborhood}
        onClick={handleClick}
      />
    );

    const card = screen.getByTestId('neighborhood-card');
    fireEvent.keyDown(card, { key: ' ' });
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('does not crash when onClick is not provided', async () => {
    render(<NeighborhoodCard neighborhood={mockNeighborhood} />);
    // Should not throw when clicked without onClick handler
    await userEvent.click(screen.getByTestId('neighborhood-card'));
  });

  it('has proper aria-label for accessibility', () => {
    render(<NeighborhoodCard neighborhood={mockNeighborhood} />);
    const card = screen.getByTestId('neighborhood-card');
    expect(card).toHaveAttribute(
      'aria-label',
      'View properties in Downtown Arts District'
    );
  });

  it('has role="button" and is focusable', () => {
    render(<NeighborhoodCard neighborhood={mockNeighborhood} />);
    const card = screen.getByTestId('neighborhood-card');
    expect(card).toHaveAttribute('role', 'button');
    expect(card).toHaveAttribute('tabindex', '0');
  });
});
