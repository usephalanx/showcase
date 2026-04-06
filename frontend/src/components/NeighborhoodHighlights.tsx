import React from 'react';

export interface NeighborhoodData {
  id: string;
  name: string;
  slug: string;
  city: string;
  state: string;
  description: string;
  image: string;
  averagePrice: number;
  walkScore: number;
  transitScore: number;
  highlights: string[];
}

export interface NeighborhoodHighlightsProps {
  neighborhoods: NeighborhoodData[];
  heading?: string;
  subheading?: string;
  onNeighborhoodClick?: (neighborhood: NeighborhoodData) => void;
}

function formatPrice(price: number): string {
  if (price >= 1_000_000) {
    return `$${(price / 1_000_000).toFixed(1)}M`;
  }
  return `$${(price / 1_000).toFixed(0)}K`;
}

const NeighborhoodHighlights: React.FC<NeighborhoodHighlightsProps> = ({
  neighborhoods,
  heading = 'Explore Neighborhoods',
  subheading,
  onNeighborhoodClick,
}) => {
  return (
    <section
      className="py-20 px-4 sm:px-6 lg:px-8 bg-stone-50"
      data-testid="neighborhood-highlights"
    >
      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="flex items-center justify-center gap-4 mb-4">
            <span className="block h-px w-12 bg-amber-600" aria-hidden="true" />
            <span className="text-sm font-semibold uppercase tracking-[0.2em] text-amber-700">
              Curated Living
            </span>
            <span className="block h-px w-12 bg-amber-600" aria-hidden="true" />
          </div>
          <h2
            className="text-3xl sm:text-4xl lg:text-5xl font-serif font-bold text-stone-900 mb-4"
            data-testid="section-heading"
          >
            {heading}
          </h2>
          {subheading && (
            <p
              className="text-lg text-stone-500 max-w-2xl mx-auto leading-relaxed"
              data-testid="section-subheading"
            >
              {subheading}
            </p>
          )}
        </div>

        {/* Neighborhood Grid */}
        <div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
          data-testid="neighborhood-grid"
        >
          {neighborhoods.map((neighborhood) => (
            <article
              key={neighborhood.id}
              className="group relative bg-white rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-500 cursor-pointer"
              data-testid={`neighborhood-card-${neighborhood.id}`}
              onClick={() => onNeighborhoodClick?.(neighborhood)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  onNeighborhoodClick?.(neighborhood);
                }
              }}
            >
              {/* Image Container */}
              <div className="relative h-64 overflow-hidden">
                <img
                  src={neighborhood.image}
                  alt={`${neighborhood.name} neighborhood`}
                  className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                  loading="lazy"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />
                <div className="absolute bottom-4 left-4 right-4">
                  <h3 className="text-xl font-serif font-bold text-white mb-1">
                    {neighborhood.name}
                  </h3>
                  <p className="text-sm text-white/80">
                    {neighborhood.city}, {neighborhood.state}
                  </p>
                </div>
              </div>

              {/* Content */}
              <div className="p-5">
                <p className="text-stone-600 text-sm leading-relaxed mb-4 line-clamp-2">
                  {neighborhood.description}
                </p>

                {/* Stats Row */}
                <div className="flex items-center justify-between border-t border-stone-100 pt-4">
                  <div className="text-center">
                    <p className="text-xs uppercase tracking-wider text-stone-400 mb-1">Avg. Price</p>
                    <p className="text-sm font-semibold text-stone-800">
                      {formatPrice(neighborhood.averagePrice)}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-xs uppercase tracking-wider text-stone-400 mb-1">Walk Score</p>
                    <p className="text-sm font-semibold text-stone-800">
                      {neighborhood.walkScore}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-xs uppercase tracking-wider text-stone-400 mb-1">Transit</p>
                    <p className="text-sm font-semibold text-stone-800">
                      {neighborhood.transitScore}
                    </p>
                  </div>
                </div>

                {/* Highlights */}
                {neighborhood.highlights.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-4">
                    {neighborhood.highlights.slice(0, 3).map((highlight) => (
                      <span
                        key={highlight}
                        className="inline-block text-xs px-2.5 py-1 bg-amber-50 text-amber-800 rounded-full font-medium"
                      >
                        {highlight}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </article>
          ))}
        </div>

        {/* Empty State */}
        {neighborhoods.length === 0 && (
          <p
            className="text-center text-stone-400 text-lg py-12"
            data-testid="empty-state"
          >
            No neighborhoods to display.
          </p>
        )}
      </div>
    </section>
  );
};

export default NeighborhoodHighlights;
