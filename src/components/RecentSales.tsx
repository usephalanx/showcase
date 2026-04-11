import React from 'react';

/**
 * Represents a single property sale record.
 */
export interface Sale {
  id: number;
  address: string;
  price: string;
  imageUrl: string;
  dateSold: string;
}

/**
 * Props for the RecentSales component.
 */
interface RecentSalesProps {
  sales?: Sale[];
}

/** Default sales data used when no sales prop is provided. */
const DEFAULT_SALES: Sale[] = [
  {
    id: 1,
    address: '123 Maple Drive, Springfield',
    price: '$450,000',
    imageUrl: '/images/sale1.jpg',
    dateSold: 'March 15, 2024',
  },
  {
    id: 2,
    address: '456 Oak Avenue, Riverside',
    price: '$620,000',
    imageUrl: '/images/sale2.jpg',
    dateSold: 'February 28, 2024',
  },
  {
    id: 3,
    address: '789 Pine Lane, Lakewood',
    price: '$385,000',
    imageUrl: '/images/sale3.jpg',
    dateSold: 'January 10, 2024',
  },
];

/**
 * RecentSales component showcases recent property sales
 * in an attractive, easy-to-scan grid format.
 *
 * Displays an empty state message when no sales data is available.
 * Uses default sales data when no sales prop is provided.
 */
const RecentSales: React.FC<RecentSalesProps> = ({ sales }) => {
  const salesData = sales !== undefined ? sales : DEFAULT_SALES;

  return (
    <div data-testid="recent-sales-section" className="recent-sales-section">
      <h2>Recent Sales</h2>
      {salesData.length === 0 ? (
        <div data-testid="empty-state" className="empty-state">
          <p>No recent sales to display.</p>
        </div>
      ) : (
        <div data-testid="sales-grid" className="sales-grid">
          {salesData.map((sale) => (
            <div key={sale.id} data-testid="sale-card" className="sale-card">
              <img
                src={sale.imageUrl}
                alt={`Property at ${sale.address}`}
                className="sale-image"
              />
              <div className="sale-details">
                <p className="sale-address">{sale.address}</p>
                <p className="sale-price">{sale.price}</p>
                <p className="sale-date">Sold: {sale.dateSold}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RecentSales;
