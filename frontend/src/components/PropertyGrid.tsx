import React from 'react';
import PropertyCard from './PropertyCard';

export interface PropertyGridItem {
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
}

export interface PropertyGridProps {
  /** Array of property objects to display */
  properties: PropertyGridItem[];
  /** Optional section heading displayed above the grid */
  title?: string;
  /** Message displayed when the properties array is empty */
  emptyMessage: string;
  /** Optional callback when a property card is clicked */
  onPropertyClick?: (property: PropertyGridItem) => void;
}

const PropertyGrid: React.FC<PropertyGridProps> = ({
  properties,
  title,
  emptyMessage,
  onPropertyClick,
}) => {
  return (
    <section className="w-full" data-testid="property-grid">
      {title && (
        <div className="mb-8 text-center" data-testid="property-grid-header">
          <h2 className="text-3xl font-bold text-gray-900 mb-3">{title}</h2>
          <div
            className="mx-auto h-1 w-20 rounded-full bg-blue-600"
            data-testid="property-grid-underline"
            aria-hidden="true"
          />
        </div>
      )}

      {properties.length === 0 ? (
        <div
          className="flex items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 px-6 py-16 text-center"
          data-testid="property-grid-empty"
        >
          <p className="text-lg text-gray-500">{emptyMessage}</p>
        </div>
      ) : (
        <div
          className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3"
          data-testid="property-grid-list"
        >
          {properties.map((property) => (
            <PropertyCard
              key={property.id}
              id={property.id}
              title={property.title}
              price={property.price}
              address={property.address}
              city={property.city}
              state={property.state}
              zipCode={property.zipCode}
              propertyType={property.propertyType}
              bedrooms={property.bedrooms}
              bathrooms={property.bathrooms}
              squareFeet={property.squareFeet}
              image={property.images[0] || ''}
              status={property.status}
              onClick={() => onPropertyClick?.(property)}
            />
          ))}
        </div>
      )}
    </section>
  );
};

export default PropertyGrid;
