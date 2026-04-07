import React from 'react';

export interface PropertyCardProps {
  /** Unsplash or any valid image URL */
  imageUrl: string;
  /** Street address of the property */
  address: string;
  /** Formatted price string, e.g. '$1.2M' */
  price: string;
  /** Sale status displayed as an overlay badge */
  status: 'SOLD';
  /** Alt text for the image; defaults to address if omitted */
  imageAlt?: string;
}

const PropertyCard: React.FC<PropertyCardProps> = ({
  imageUrl,
  address,
  price,
  status,
  imageAlt,
}) => {
  return (
    <div
      data-testid="property-card"
      className="group relative w-full max-w-sm rounded-xl overflow-hidden bg-white shadow-md transition-all duration-300 ease-in-out hover:shadow-xl hover:scale-[1.02] cursor-pointer"
    >
      {/* Image Container */}
      <div className="relative aspect-[4/3] w-full overflow-hidden">
        <img
          src={imageUrl}
          alt={imageAlt || address}
          className="h-full w-full object-cover transition-transform duration-500 ease-in-out group-hover:scale-110"
          loading="lazy"
        />

        {/* Status Badge Overlay */}
        <span
          data-testid="status-badge"
          className="absolute top-3 left-3 inline-flex items-center rounded px-3 py-1 text-xs font-bold uppercase tracking-widest"
          style={{
            backgroundColor: '#1E293B',
            color: '#C8A951',
          }}
        >
          {status}
        </span>

        {/* Gradient overlay at bottom of image for readability */}
        <div className="absolute inset-x-0 bottom-0 h-16 bg-gradient-to-t from-black/30 to-transparent pointer-events-none" />
      </div>

      {/* Content */}
      <div className="px-4 py-4">
        <p
          data-testid="property-address"
          className="text-sm text-gray-600 leading-snug line-clamp-2"
          style={{ fontFamily: "'Inter', sans-serif" }}
        >
          {address}
        </p>
        <p
          data-testid="property-price"
          className="mt-1 text-lg font-bold text-gray-900"
          style={{ fontFamily: "'Playfair Display', serif" }}
        >
          {price}
        </p>
      </div>
    </div>
  );
};

export default PropertyCard;
