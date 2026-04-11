import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import RecentSales, { Sale } from '../components/RecentSales';

describe('RecentSales Component', () => {
  const mockSales: Sale[] = [
    {
      id: 1,
      address: '100 Test Street, Testville',
      price: '$500,000',
      imageUrl: '/sales/test1.jpg',
      date: 'March 2024',
      status: 'Sold',
    },
    {
      id: 2,
      address: '200 Example Lane, Sampletown',
      price: '$750,000',
      imageUrl: '/sales/test2.jpg',
      date: 'February 2024',
      status: 'Pending',
    },
  ];

  describe('Rendering with sales data', () => {
    it('renders the section heading', () => {
      render(<RecentSales sales={mockSales} />);
      expect(screen.getByText('Recent Sales')).toBeInTheDocument();
    });

    it('renders the correct number of sale cards', () => {
      render(<RecentSales sales={mockSales} />);
      const cards = screen.getAllByTestId('sale-card');
      expect(cards).toHaveLength(2);
    });

    it('renders the section element with correct test id', () => {
      render(<RecentSales sales={mockSales} />);
      expect(screen.getByTestId('recent-sales-section')).toBeInTheDocument();
    });

    it('displays each sale address', () => {
      render(<RecentSales sales={mockSales} />);
      expect(screen.getByText('100 Test Street, Testville')).toBeInTheDocument();
      expect(screen.getByText('200 Example Lane, Sampletown')).toBeInTheDocument();
    });

    it('displays each sale price', () => {
      render(<RecentSales sales={mockSales} />);
      expect(screen.getByText('$500,000')).toBeInTheDocument();
      expect(screen.getByText('$750,000')).toBeInTheDocument();
    });

    it('displays each sale date', () => {
      render(<RecentSales sales={mockSales} />);
      expect(screen.getByText('March 2024')).toBeInTheDocument();
      expect(screen.getByText('February 2024')).toBeInTheDocument();
    });

    it('displays the sale status', () => {
      render(<RecentSales sales={mockSales} />);
      const statuses = screen.getAllByTestId('sale-status');
      expect(statuses[0]).toHaveTextContent('Sold');
      expect(statuses[1]).toHaveTextContent('Pending');
    });

    it('renders images with correct alt text', () => {
      render(<RecentSales sales={mockSales} />);
      expect(screen.getByAlt('Property at 100 Test Street, Testville')).toBeInTheDocument();
      expect(screen.getByAlt('Property at 200 Example Lane, Sampletown')).toBeInTheDocument();
    });

    it('renders the sales grid container', () => {
      render(<RecentSales sales={mockSales} />);
      expect(screen.getByTestId('sales-grid')).toBeInTheDocument();
    });

    it('does not render empty state when sales are present', () => {
      render(<RecentSales sales={mockSales} />);
      expect(screen.queryByTestId('empty-state')).not.toBeInTheDocument();
    });
  });

  describe('Rendering with empty sales data', () => {
    it('renders empty state message when sales array is empty', () => {
      render(<RecentSales sales={[]} />);
      expect(screen.getByTestId('empty-state')).toBeInTheDocument();
      expect(screen.getByText('No recent sales to display at this time.')).toBeInTheDocument();
    });

    it('does not render any sale cards when sales is empty', () => {
      render(<RecentSales sales={[]} />);
      expect(screen.queryByTestId('sale-card')).not.toBeInTheDocument();
    });

    it('does not render sales grid when sales is empty', () => {
      render(<RecentSales sales={[]} />);
      expect(screen.queryByTestId('sales-grid')).not.toBeInTheDocument();
    });

    it('still renders the section heading with empty sales', () => {
      render(<RecentSales sales={[]} />);
      expect(screen.getByText('Recent Sales')).toBeInTheDocument();
    });
  });

  describe('Default sales data', () => {
    it('renders default sales when no props are provided', () => {
      render(<RecentSales />);
      const cards = screen.getAllByTestId('sale-card');
      expect(cards.length).toBeGreaterThan(0);
    });

    it('shows default addresses when no sales prop given', () => {
      render(<RecentSales />);
      expect(screen.getByText('123 Oak Avenue, Springfield')).toBeInTheDocument();
      expect(screen.getByText('456 Maple Drive, Riverside')).toBeInTheDocument();
      expect(screen.getByText('789 Pine Street, Lakewood')).toBeInTheDocument();
    });
  });

  describe('Sale status defaults', () => {
    it('defaults to "Sold" when status is not provided', () => {
      const salesWithoutStatus: Sale[] = [
        {
          id: 1,
          address: '999 Default Status Road',
          price: '$300,000',
          imageUrl: '/sales/default.jpg',
          date: 'April 2024',
        },
      ];
      render(<RecentSales sales={salesWithoutStatus} />);
      const status = screen.getByTestId('sale-status');
      expect(status).toHaveTextContent('Sold');
    });
  });

  describe('Image error handling', () => {
    it('hides image on error and shows fallback', () => {
      render(<RecentSales sales={mockSales} />);
      const images = screen.getAllByRole('img');
      fireEvent.error(images[0]);
      expect(images[0].style.display).toBe('none');
    });
  });

  describe('Single sale rendering', () => {
    it('renders correctly with a single sale', () => {
      const singleSale: Sale[] = [
        {
          id: 42,
          address: '1 Lonely Lane',
          price: '$999,999',
          imageUrl: '/sales/lonely.jpg',
          date: 'May 2024',
          status: 'Sold',
        },
      ];
      render(<RecentSales sales={singleSale} />);
      expect(screen.getAllByTestId('sale-card')).toHaveLength(1);
      expect(screen.getByText('1 Lonely Lane')).toBeInTheDocument();
      expect(screen.getByText('$999,999')).toBeInTheDocument();
    });
  });
});
