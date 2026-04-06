import React from 'react';
import type { Neighborhood } from '../types/models';

export interface NeighborhoodCardProps {
  /** The neighborhood data to display */
  neighborhood: Neighborhood;
  /** Callback invoked when the card is clicked */
  onClick?: (neighborhood: Neighborhood) => void;
}

function formatPrice(price: number): string {
  if (price >= 1_000_000) {
    const millions = price / 1_000_000;
    return `$${millions % 1 === 0 ? millions.toFixed(0) : millions.toFixed(1)}M`;
  }
  if (price >= 1_000) {
    return `$${(price / 1_000).toFixed(0)}K`;
  }
  return `$${price.toLocaleString()}`;
}

const NeighborhoodCard: React.FC<NeighborhoodCardProps> = ({
  neighborhood,
  onClick,
}) => {
  const handleClick = () => {
    if (onClick) {
      onClick(neighborhood);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  };

  return (
    <div
      role="button"
      tabIndex={0}
      aria-label={`View properties in ${neighborhood.name}`}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      className="group relative overflow-hidden rounded-xl cursor-pointer
        transition-all duration-300 ease-out
        hover:-translate-y-2 hover:shadow-2xl
        focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
      style={{ minHeight: '320px' }}
      data-testid="neighborhood-card"
    >
      {/* Background Image */}
      <div
        className="absolute inset-0 bg-cover bg-center transition-transform duration-500 ease-out group-hover:scale-110"
        style={{ backgroundImage: `url(${neighborhood.image})` }}
        data-testid="neighborhood-card-image"
      />

      {/* Dark Gradient Overlay */}
      <div
        className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent
          transition-opacity duration-300 group-hover:from-black/85 group-hover:via-black/50"
        data-testid="neighborhood-card-overlay"
      />

      {/* Content */}
      <div className="relative h-full flex flex-col justify-end p-6" style={{ minHeight: '320px' }}>
        {/* City & State Badge */}
        <span
          className="self-start mb-2 inline-block rounded-full bg-white/20 backdrop-blur-sm
            px-3 py-1 text-xs font-medium text-white tracking-wide uppercase"
          data-testid="neighborhood-card-location"
        >
          {neighborhood.city}, {neighborhood.state}
        </span>

        {/* Neighborhood Name */}
        <h3
          className="text-2xl font-bold text-white mb-2 leading-tight
            transition-colors duration-300 group-hover:text-blue-200"
          data-testid="neighborhood-card-name"
        >
          {neighborhood.name}
        </h3>

        {/* Stats Row */}
        <div className="flex items-center gap-4 text-white/90">
          <div className="flex items-center gap-1.5" data-testid="neighborhood-card-price">
            <svg
              className="w-4 h-4 text-blue-300"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span className="text-sm font-semibold">
              Avg. {formatPrice(neighborhood.averagePrice)}
            </span>
          </div>

          <div className="w-px h-4 bg-white/30" aria-hidden="true" />

          <div className="flex items-center gap-1.5" data-testid="neighborhood-card-count">
            <svg
              className="w-4 h-4 text-blue-300"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1h-2z"
              />
            </svg>
            <span className="text-sm font-semibold">
              {neighborhood.propertyCount} {neighborhood.propertyCount === 1 ? 'Property' : 'Properties'}
            </span>
          </div>
        </div>

        {/* Explore Arrow — visible on hover */}
        <div
          className="mt-3 flex items-center gap-1 text-blue-300 text-sm font-medium
            opacity-0 translate-y-2 transition-all duration-300
            group-hover:opacity-100 group-hover:translate-y-0"
          aria-hidden="true"
        >
          <span>Explore neighborhood</span>
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </div>
      </div>
    </div>
  );
};

export default NeighborhoodCard;
