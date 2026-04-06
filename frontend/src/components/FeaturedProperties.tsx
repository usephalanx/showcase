import React from 'react';

export interface Property {
  id: string;
  title: string;
  slug: string;
  price: number;
  address: string;
  city: string;
  state: string;
  zipCode: string;
  propertyType: 'house' | 'condo' | 'townhouse' | 'apartment' | 'land';
  bedrooms: number;
  bathrooms: number;
  squareFeet: number;
  lotSize?: string;
  yearBuilt?: number;
  description: string;
  features: string[];
  images: string[];
  listingDate: string;
  status: 'for-sale' | 'pending' | 'sold';
  featured?: boolean;
}

export interface FeaturedPropertiesProps {
  /** Full list of properties; only those with featured=true are displayed */
  properties: Property[];
  /** Optional section heading override (defaults to "Featured Properties") */
  heading?: string;
  /** Optional subheading text beneath the heading */
  subheading?: string;
  /** Label for the call-to-action button (defaults to "View All Properties") */
  viewAllLabel?: string;
  /** Callback fired when the "View All Properties" button/link is clicked */
  onViewAll?: () => void;
  /** Optional href for the "View All Properties" link (used if no onViewAll provided) */
  viewAllHref?: string;
  /** Callback fired when a property card is clicked */
  onPropertyClick?: (property: Property) => void;
}

function formatPrice(price: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(price);
}

function PropertyCard({
  property,
  onClick,
}: {
  property: Property;
  onClick?: (property: Property) => void;
}) {
  const mainImage = property.images[0] || 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop';

  return (
    <div
      className="featured-property-card"
      role="article"
      aria-label={property.title}
      onClick={() => onClick?.(property)}
      style={{
        cursor: onClick ? 'pointer' : 'default',
        borderRadius: '12px',
        overflow: 'hidden',
        boxShadow: '0 4px 16px rgba(0, 0, 0, 0.1)',
        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
        backgroundColor: '#fff',
      }}
    >
      <div style={{ position: 'relative', overflow: 'hidden', height: '220px' }}>
        <img
          src={mainImage}
          alt={property.title}
          loading="lazy"
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        <span
          style={{
            position: 'absolute',
            top: '12px',
            left: '12px',
            backgroundColor: '#e53e3e',
            color: '#fff',
            fontSize: '0.75rem',
            fontWeight: 600,
            padding: '4px 10px',
            borderRadius: '4px',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
          }}
        >
          Featured
        </span>
        <span
          style={{
            position: 'absolute',
            bottom: '12px',
            right: '12px',
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            color: '#fff',
            fontSize: '1.125rem',
            fontWeight: 700,
            padding: '6px 14px',
            borderRadius: '6px',
          }}
        >
          {formatPrice(property.price)}
        </span>
      </div>
      <div style={{ padding: '16px 20px 20px' }}>
        <h3 style={{ margin: '0 0 6px', fontSize: '1.125rem', fontWeight: 700, color: '#1a202c' }}>
          {property.title}
        </h3>
        <p style={{ margin: '0 0 12px', fontSize: '0.875rem', color: '#718096' }}>
          {property.address}, {property.city}, {property.state} {property.zipCode}
        </p>
        <div
          style={{
            display: 'flex',
            gap: '16px',
            fontSize: '0.85rem',
            color: '#4a5568',
          }}
        >
          <span data-testid="bedrooms">{property.bedrooms} Beds</span>
          <span data-testid="bathrooms">{property.bathrooms} Baths</span>
          <span data-testid="sqft">{property.squareFeet.toLocaleString()} Sq Ft</span>
        </div>
      </div>
    </div>
  );
}

export default function FeaturedProperties({
  properties,
  heading = 'Featured Properties',
  subheading,
  viewAllLabel = 'View All Properties',
  onViewAll,
  viewAllHref = '/properties',
  onPropertyClick,
}: FeaturedPropertiesProps) {
  const featuredProperties = properties.filter((p) => p.featured);

  return (
    <section aria-labelledby="featured-properties-heading" style={{ padding: '64px 24px', maxWidth: '1200px', margin: '0 auto' }}>
      {/* Decorative heading */}
      <div style={{ textAlign: 'center', marginBottom: '48px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px', marginBottom: '8px' }}>
          <span aria-hidden="true" style={{ display: 'inline-block', width: '48px', height: '2px', backgroundColor: '#e53e3e' }} />
          <span aria-hidden="true" style={{ fontSize: '1.25rem', color: '#e53e3e' }}>★</span>
          <span aria-hidden="true" style={{ display: 'inline-block', width: '48px', height: '2px', backgroundColor: '#e53e3e' }} />
        </div>
        <h2
          id="featured-properties-heading"
          style={{ margin: '0 0 8px', fontSize: '2rem', fontWeight: 800, color: '#1a202c' }}
        >
          {heading}
        </h2>
        {subheading && (
          <p style={{ margin: 0, fontSize: '1.1rem', color: '#718096', maxWidth: '600px', marginLeft: 'auto', marginRight: 'auto' }}>
            {subheading}
          </p>
        )}
      </div>

      {/* Property Grid */}
      {featuredProperties.length === 0 ? (
        <p style={{ textAlign: 'center', color: '#a0aec0', fontSize: '1rem' }} data-testid="no-featured">
          No featured properties available at this time.
        </p>
      ) : (
        <div
          data-testid="property-grid"
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
            gap: '32px',
          }}
        >
          {featuredProperties.map((property) => (
            <PropertyCard key={property.id} property={property} onClick={onPropertyClick} />
          ))}
        </div>
      )}

      {/* View All CTA */}
      <div style={{ textAlign: 'center', marginTop: '48px' }}>
        {onViewAll ? (
          <button
            type="button"
            onClick={onViewAll}
            style={{
              display: 'inline-block',
              padding: '14px 36px',
              fontSize: '1rem',
              fontWeight: 600,
              color: '#fff',
              backgroundColor: '#2b6cb0',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              transition: 'background-color 0.2s ease',
            }}
          >
            {viewAllLabel}
          </button>
        ) : (
          <a
            href={viewAllHref}
            style={{
              display: 'inline-block',
              padding: '14px 36px',
              fontSize: '1rem',
              fontWeight: 600,
              color: '#fff',
              backgroundColor: '#2b6cb0',
              borderRadius: '8px',
              textDecoration: 'none',
              transition: 'background-color 0.2s ease',
            }}
          >
            {viewAllLabel}
          </a>
        )}
      </div>
    </section>
  );
}
