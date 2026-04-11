import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { RecentSales, Sale } from '../components/RecentSales';

const mockSales: Sale[] = [
  {
    id: 1,
    address: '100 Test Lane, Testville',
    price: '$500,000',
    imageUrl: '/logo.svg',
    soldDate: '2024-02-01',
  },
  {
    id: 2,
    address: '200 Sample Road, Mocktown',
    price: '$750,000',
    imageUrl: '/logo.svg',
    soldDate: '2024-01-20',
  },
];

describe('RecentSales', () => {
  it('renders the section heading', () => {
    render(<RecentSales sales={mockSales} />);
    expect(screen.getByText('Recent Sales')).toBeInTheDocument();
  });

  it('renders all sale cards when sales data is provided', () => {
    render(<RecentSales sales={mockSales} />);
    const cards = screen.getAllByTestId('sale-card');
    expect(cards).toHaveLength(2);
  });

  it('renders sale addresses', () => {
    render(<RecentSales sales={mockSales} />);
    expect(screen.getByText('100 Test Lane, Testville')).toBeInTheDocument();
    expect(screen.getByText('200 Sample Road, Mocktown')).toBeInTheDocument();
  });

  it('renders sale prices', () => {
    render(<RecentSales sales={mockSales} />);
    expect(screen.getByText('$500,000')).toBeInTheDocument();
    expect(screen.getByText('$750,000')).toBeInTheDocument();
  });

  it('renders empty state when sales is an empty array', () => {
    render(<RecentSales sales={[]} />);
    expect(screen.getByTestId('empty-state')).toBeInTheDocument();
    expect(
      screen.getByText('No recent sales to display at this time.'),
    ).toBeInTheDocument();
  });

  it('renders empty state when sales is null', () => {
    render(<RecentSales sales={null} />);
    expect(screen.getByTestId('empty-state')).toBeInTheDocument();
  });

  it('renders default sales when no sales prop is provided', () => {
    render(<RecentSales />);
    const cards = screen.getAllByTestId('sale-card');
    expect(cards.length).toBeGreaterThan(0);
  });
});
