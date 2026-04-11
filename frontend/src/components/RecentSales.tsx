import React from 'react';

/** Represents a single property sale record. */
export interface Sale {
  id: number;
  address: string;
  price: string;
  imageUrl: string;
  soldDate: string;
}

/** Props for the RecentSales component. */
export interface RecentSalesProps {
  sales?: Sale[] | null;
}

/** Default sample sales data used when no props are provided. */
const DEFAULT_SALES: Sale[] = [
  {
    id: 1,
    address: '123 Oak Avenue, Springfield',
    price: '$450,000',
    imageUrl: '/logo.svg',
    soldDate: '2024-01-15',
  },
  {
    id: 2,
    address: '456 Maple Drive, Riverside',
    price: '$625,000',
    imageUrl: '/logo.svg',
    soldDate: '2024-01-10',
  },
  {
    id: 3,
    address: '789 Pine Street, Lakeview',
    price: '$380,000',
    imageUrl: '/logo.svg',
    soldDate: '2024-01-05',
  },
];

/**
 * RecentSales component.
 * Showcases recent property sales in an attractive grid format.
 * Supports an empty state when no sales data is available.
 */
export const RecentSales: React.FC<RecentSalesProps> = ({ sales }) => {
  const displaySales = sales === undefined ? DEFAULT_SALES : sales;

  return (
    <section className="recent-sales-section" data-testid="recent-sales">
      <h2 className="section-heading">Recent Sales</h2>

      {!displaySales || displaySales.length === 0 ? (
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
                className="sale-image"
                width={300}
                height={200}
              />
              <div className="sale-details">
                <h3 className="sale-address">{sale.address}</h3>
                <p className="sale-price">{sale.price}</p>
                <p className="sale-date">Sold: {sale.soldDate}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};
