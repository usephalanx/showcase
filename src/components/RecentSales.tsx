import React from 'react';

/** Represents a single property sale record. */
export interface Sale {
  /** Unique identifier for the sale. */
  id: number;
  /** Street address of the property. */
  address: string;
  /** Sale price formatted as a string (e.g. "$450,000"). */
  price: string;
  /** URL for the property image. */
  imageUrl: string;
  /** Date string for when the sale closed. */
  dateSold: string;
}

/** Props for the RecentSales component. */
export interface RecentSalesProps {
  /** Optional array of sales to display. Falls back to default data if not provided. */
  sales?: Sale[];
}

/** Default sample sales data displayed when no explicit sales prop is provided. */
const DEFAULT_SALES: Sale[] = [
  {
    id: 1,
    address: '123 Maple Drive, Springfield',
    price: '$450,000',
    imageUrl: 'https://via.placeholder.com/400x200?text=Property+1',
    dateSold: 'January 15, 2024',
  },
  {
    id: 2,
    address: '456 Oak Avenue, Shelbyville',
    price: '$625,000',
    imageUrl: 'https://via.placeholder.com/400x200?text=Property+2',
    dateSold: 'February 3, 2024',
  },
  {
    id: 3,
    address: '789 Pine Lane, Capital City',
    price: '$380,000',
    imageUrl: 'https://via.placeholder.com/400x200?text=Property+3',
    dateSold: 'March 20, 2024',
  },
];

/**
 * RecentSales component displays a responsive grid of recent property sales.
 * Supports both populated and empty states. Accepts an optional `sales` prop;
 * when omitted, default sample data is rendered.
 */
const RecentSales: React.FC<RecentSalesProps> = ({ sales }) => {
  const displaySales = sales !== undefined ? sales : DEFAULT_SALES;

  return (
    <section className="recent-sales-section" data-testid="recent-sales-section" aria-label="Recent Sales">
      <h2>Recent Sales</h2>
      {displaySales.length === 0 ? (
        <div className="empty-state" data-testid="empty-state">
          <p>No recent sales to display at this time.</p>
        </div>
      ) : (
        <div className="sales-grid" data-testid="sales-grid">
          {displaySales.map((sale) => (
            <article key={sale.id} className="sale-card" data-testid="sale-card">
              <img src={sale.imageUrl} alt={`Property at ${sale.address}`} />
              <div className="sale-card-info">
                <p className="sale-address">{sale.address}</p>
                <p className="sale-price">{sale.price}</p>
                <p className="sale-date">Sold: {sale.dateSold}</p>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
};

export default RecentSales;
