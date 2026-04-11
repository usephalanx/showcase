import React from 'react';
import { render, screen, within } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import RecentSales, { Sale } from '../components/RecentSales';

describe('RecentSales', () => {
  it('renders default sales when no props provided', () => {
    render(<RecentSales />);
    const section = screen.getByTestId('recent-sales-section');
    expect(within(section).getByText('Recent Sales')).toBeInTheDocument();
    const cards = within(section).getAllByTestId('sale-card');
    expect(cards.length).toBe(3);
  });

  it('renders provided sales data', () => {
    const sales: Sale[] = [
      {
        id: 10,
        address: '1 Test Lane',
        price: '$100,000',
        imageUrl: '/test.jpg',
        date: 'March 2024',
      },
      {
        id: 11,
        address: '2 Test Lane',
        price: '$200,000',
        imageUrl: '/test2.jpg',
        date: 'April 2024',
      },
    ];

    render(<RecentSales sales={sales} />);
    const cards = screen.getAllByTestId('sale-card');
    expect(cards.length).toBe(2);
    expect(screen.getByText('1 Test Lane')).toBeInTheDocument();
    expect(screen.getByText('$100,000')).toBeInTheDocument();
    expect(screen.getByText('2 Test Lane')).toBeInTheDocument();
    expect(screen.getByText('$200,000')).toBeInTheDocument();
  });

  it('shows empty state when sales array is empty', () => {
    render(<RecentSales sales={[]} />);
    expect(screen.getByTestId('empty-state')).toHaveTextContent(
      'No recent sales to display at this time.'
    );
    expect(screen.queryByTestId('sale-card')).not.toBeInTheDocument();
  });

  it('displays address, price, and date for each sale', () => {
    const sales: Sale[] = [
      {
        id: 1,
        address: '42 Wallaby Way, Sydney',
        price: '$999,999',
        imageUrl: '/img.jpg',
        date: 'June 2024',
      },
    ];

    render(<RecentSales sales={sales} />);
    const card = screen.getByTestId('sale-card');
    expect(within(card).getByText('42 Wallaby Way, Sydney')).toBeInTheDocument();
    expect(within(card).getByText('$999,999')).toBeInTheDocument();
    expect(within(card).getByText('June 2024')).toBeInTheDocument();
  });

  it('renders images with correct alt text', () => {
    const sales: Sale[] = [
      {
        id: 1,
        address: '10 Downing Street',
        price: '$1,000,000',
        imageUrl: '/house.jpg',
        date: 'May 2024',
      },
    ];

    render(<RecentSales sales={sales} />);
    const img = screen.getByAlt('Property at 10 Downing Street');
    expect(img).toBeInTheDocument();
    expect(img).toHaveAttribute('src', '/house.jpg');
  });
});
