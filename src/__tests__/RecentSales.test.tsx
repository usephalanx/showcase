import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import RecentSales, { Sale } from '../components/RecentSales';

/**
 * Test suite for the RecentSales component.
 * Covers rendering with data, empty state, and default data.
 */
describe('RecentSales', () => {
  const sampleSales: Sale[] = [
    {
      id: 1,
      address: '10 Test Street, TestCity',
      price: '$100,000',
      imageUrl: 'https://via.placeholder.com/400x200?text=Test',
      dateSold: 'April 1, 2024',
    },
    {
      id: 2,
      address: '20 Sample Ave, SampleTown',
      price: '$250,000',
      imageUrl: 'https://via.placeholder.com/400x200?text=Test2',
      dateSold: 'May 10, 2024',
    },
  ];

  it('renders the section heading', () => {
    render(<RecentSales sales={sampleSales} />);
    expect(screen.getByRole('heading', { name: /recent sales/i })).toBeInTheDocument();
  });

  it('renders all sale cards when sales data is provided', () => {
    render(<RecentSales sales={sampleSales} />);
    const cards = screen.getAllByTestId('sale-card');
    expect(cards).toHaveLength(2);
  });

  it('displays address, price, and date for each sale', () => {
    render(<RecentSales sales={sampleSales} />);
    expect(screen.getByText('10 Test Street, TestCity')).toBeInTheDocument();
    expect(screen.getByText('$100,000')).toBeInTheDocument();
    expect(screen.getByText('Sold: April 1, 2024')).toBeInTheDocument();
    expect(screen.getByText('20 Sample Ave, SampleTown')).toBeInTheDocument();
    expect(screen.getByText('$250,000')).toBeInTheDocument();
  });

  it('renders images with proper alt text', () => {
    render(<RecentSales sales={sampleSales} />);
    expect(screen.getByAltText('Property at 10 Test Street, TestCity')).toBeInTheDocument();
    expect(screen.getByAltText('Property at 20 Sample Ave, SampleTown')).toBeInTheDocument();
  });

  it('renders the empty state when sales array is empty', () => {
    render(<RecentSales sales={[]} />);
    expect(screen.getByTestId('empty-state')).toBeInTheDocument();
    expect(screen.getByText(/no recent sales to display/i)).toBeInTheDocument();
  });

  it('does not render the sales grid when sales array is empty', () => {
    render(<RecentSales sales={[]} />);
    expect(screen.queryByTestId('sales-grid')).not.toBeInTheDocument();
  });

  it('renders default sales data when no sales prop is provided', () => {
    render(<RecentSales />);
    const cards = screen.getAllByTestId('sale-card');
    expect(cards.length).toBeGreaterThan(0);
  });

  it('does not show empty state when default data is used', () => {
    render(<RecentSales />);
    expect(screen.queryByTestId('empty-state')).not.toBeInTheDocument();
  });
});
