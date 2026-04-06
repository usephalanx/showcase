import React from 'react';
import { Bed, Bath, Square } from 'lucide-react';
import { Property } from '../types/models';

export interface PropertyCardProps {
  /** The property data to display */
  property: Property;
  /** Optional click handler for navigating to the property detail */
  onViewDetail?: (slug: string) => void;
  /** Optional className for the outer container */
  className?: string;
}

function formatPrice(price: number): string {
  return price.toLocaleString('en-US');
}

function formatSquareFeet(sqft: number): string {
  return sqft.toLocaleString('en-US');
}

const PropertyCard: React.FC<PropertyCardProps> = ({
  property,
  onViewDetail,
  className = '',
}) => {
  const {
    title,
    slug,
    price,
    address,
    city,
    state,
    zipCode,
    bedrooms,
    bathrooms,
    squareFeet,
    images,
    status,
    isFeatured,
  } = property;

  const primaryImage = images.length > 0 ? images[0] : '';
  const fullAddress = `${address}, ${city}, ${state} ${zipCode}`;

  const handleClick = () => {
    if (onViewDetail) {
      onViewDetail(slug);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  };

  const statusLabel: Record<string, string> = {
    'for-sale': 'For Sale',
    pending: 'Pending',
    sold: 'Sold',
  };

  return (
    <div
      className={
        `group relative flex flex-col overflow-hidden rounded-xl bg-white shadow-md ` +
        `transition-shadow duration-300 hover:shadow-xl cursor-pointer ${className}`
      }
      role="link"
      tabIndex={0}
      aria-label={`View details for ${title}`}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      data-testid="property-card"
    >
      {/* Image Container */}
      <div className="relative h-56 w-full overflow-hidden">
        {primaryImage && (
          <img
            src={primaryImage}
            alt={title}
            className={
              `h-full w-full object-cover transition-transform duration-500 ` +
              `ease-in-out group-hover:scale-110`
            }
            loading="lazy"
          />
        )}

        {/* Featured Badge */}
        {isFeatured && (
          <span
            className={
              `absolute top-3 left-3 rounded-full bg-amber-500 px-3 py-1 ` +
              `text-xs font-semibold uppercase tracking-wide text-white shadow-sm`
            }
            data-testid="featured-badge"
          >
            Featured
          </span>
        )}

        {/* Status Badge */}
        <span
          className={
            `absolute top-3 right-3 rounded-full px-3 py-1 text-xs font-semibold ` +
            `uppercase tracking-wide text-white shadow-sm ${
              status === 'for-sale'
                ? 'bg-emerald-600'
                : status === 'pending'
                  ? 'bg-yellow-600'
                  : 'bg-red-600'
            }`
          }
          data-testid="status-badge"
        >
          {statusLabel[status] ?? status}
        </span>
      </div>

      {/* Content */}
      <div className="flex flex-1 flex-col p-5">
        {/* Price */}
        <p
          className="text-2xl font-bold text-slate-900"
          data-testid="property-price"
        >
          ${formatPrice(price)}
        </p>

        {/* Address */}
        <p
          className="mt-1 text-sm text-slate-500 line-clamp-1"
          title={fullAddress}
          data-testid="property-address"
        >
          {fullAddress}
        </p>

        {/* Divider */}
        <hr className="my-3 border-slate-200" />

        {/* Info Row */}
        <div
          className="flex items-center gap-4 text-sm text-slate-600"
          data-testid="property-info-row"
        >
          <div className="flex items-center gap-1.5" title={`${bedrooms} bedrooms`}>
            <Bed className="h-4 w-4 text-slate-400" aria-hidden="true" />
            <span data-testid="property-beds">{bedrooms}</span>
            <span className="sr-only">bedrooms</span>
          </div>

          <div className="flex items-center gap-1.5" title={`${bathrooms} bathrooms`}>
            <Bath className="h-4 w-4 text-slate-400" aria-hidden="true" />
            <span data-testid="property-baths">{bathrooms}</span>
            <span className="sr-only">bathrooms</span>
          </div>

          <div
            className="flex items-center gap-1.5"
            title={`${formatSquareFeet(squareFeet)} sq ft`}
          >
            <Square className="h-4 w-4 text-slate-400" aria-hidden="true" />
            <span data-testid="property-sqft">
              {formatSquareFeet(squareFeet)}
            </span>
            <span className="text-slate-400">sqft</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PropertyCard;
