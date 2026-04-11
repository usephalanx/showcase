import React from 'react';

/** Represents a single property sale record. */
export interface Sale {
  /** Unique identifier for the sale. */
  id: number;
  /** Street address of the sold property. */
  address: string;
  /** Sale price as a formatted string (e.g. "$450,000"). */
  price: string;
  /** URL of the property image. */
  imageUrl: string;
  /** Date when the sale was completed. */
  date: string;
}

/** Default sales data used when no props are provided. */
const defaultSales: Sale[] = [
  {
    id: 1,
    address: '123 Oak Avenue, Springfield',
    price: '$450,000',
    imageUrl: '/sales/house1.jpg',
    date: 'January 2024',
  },
  {
    id: 2,
    address: '456 Maple Drive, Riverside',
    price: '$625,000',
    imageUrl: '/sales/house2.jpg',
    date: 'December 2023',
  },
  {
    id: 3,
    address: '789 Pine Street, Lakewood',
    price: '$380,000',
    imageUrl: '/sales/house3.jpg',
    date: 'November 2023',
  },
];

/** Props for the RecentSales component. */
interface RecentSalesProps {
  /** Optional array of sales to display. Falls back to default data if not provided. */
  sales?: Sale[];
}

/**
 * RecentSales component showcases recent property sales in a responsive
 * grid layout. Displays an empty-state message when no sales data is available.
 */
const RecentSales: React.FC<RecentSalesProps> = ({ sales }) => {
  const displaySales = sales !== undefined ? sales : defaultSales;

  return (
    <section className="section recent-sales-section" data-testid="recent-sales-section">
      <h2>Recent Sales</h2>
      {displaySales.length === 0 ? (
        <p className="empty-state" data-testid="empty-state">
          No recent sales to display at this time.
        </p>
      ) : (
        <div className="sales-grid">
          {displaySales.map((sale) => (
            <div key={sale.id} className="sale-card" data-testid="sale-card">
              <img
                src={sale.imageUrl}
                alt={`Property at ${sale.address}`}
                onError={(e) => {
                  const target = e.currentTarget;
                  target.style.display = 'none';
                }}
              />
              <div className="sale-card-body">
                <p className="sale-address">{sale.address}</p>
                <p className="sale-price">{sale.price}</p>
                <p className="sale-date">{sale.date}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};

export default RecentSales;
