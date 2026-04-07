import React from 'react';

export interface PropertyCardData {
  imageUrl: string;
  address: string;
  price: string;
  status: 'SOLD' | 'FOR SALE' | 'PENDING';
}

export interface RecentSalesProps {
  /** The id attribute applied to the section wrapper */
  sectionId?: string;
  /** Section heading text */
  heading?: string;
  /** Array of property card data to render */
  properties?: PropertyCardData[];
}

const DEFAULT_PROPERTIES: PropertyCardData[] = [
  {
    imageUrl: 'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800&q=80',
    address: '742 Evergreen Terrace, Beverly Hills',
    price: '$1.2M',
    status: 'SOLD',
  },
  {
    imageUrl: 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80',
    address: '1201 Ocean Avenue, Malibu',
    price: '$875K',
    status: 'SOLD',
  },
  {
    imageUrl: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80',
    address: '88 Sunset Boulevard, Pacific Palisades',
    price: '$2.1M',
    status: 'SOLD',
  },
];

function SectionWrapper({
  id,
  children,
}: {
  id: string;
  children: React.ReactNode;
}) {
  return (
    <section
      id={id}
      className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-20 lg:py-24"
    >
      {children}
    </section>
  );
}

function PropertyCard({ imageUrl, address, price, status }: PropertyCardData) {
  const statusColors: Record<string, string> = {
    SOLD: 'bg-red-600',
    'FOR SALE': 'bg-green-600',
    PENDING: 'bg-yellow-600',
  };

  return (
    <div
      className="group rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300 bg-white"
      data-testid="property-card"
    >
      <div className="relative overflow-hidden">
        <img
          src={imageUrl}
          alt={address}
          className="w-full h-56 sm:h-64 object-cover group-hover:scale-105 transition-transform duration-500"
          loading="lazy"
        />
        <span
          className={`absolute top-3 left-3 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-white rounded ${statusColors[status] || 'bg-gray-600'}`}
          data-testid="property-status"
        >
          {status}
        </span>
      </div>
      <div className="p-5">
        <h3
          className="text-base sm:text-lg font-medium text-slate-800 leading-snug mb-2"
          data-testid="property-address"
        >
          {address}
        </h3>
        <p
          className="text-xl sm:text-2xl font-bold text-slate-900"
          style={{ fontFamily: "'Playfair Display', serif" }}
          data-testid="property-price"
        >
          {price}
        </p>
      </div>
    </div>
  );
}

const RecentSales: React.FC<RecentSalesProps> = ({
  sectionId = 'listings',
  heading = 'Recent Sales',
  properties = DEFAULT_PROPERTIES,
}) => {
  return (
    <SectionWrapper id={sectionId}>
      <h2
        className="text-3xl sm:text-4xl lg:text-5xl font-bold text-center mb-12 sm:mb-16 text-slate-900"
        style={{ fontFamily: "'Playfair Display', serif" }}
        data-testid="section-heading"
      >
        {heading}
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
        {properties.map((property, index) => (
          <PropertyCard key={`${property.address}-${index}`} {...property} />
        ))}
      </div>
    </SectionWrapper>
  );
};

export default RecentSales;
