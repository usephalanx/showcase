/**
 * LoadingSkeleton – animated placeholder cards shown while projects are loading.
 */

import React from 'react';

interface LoadingSkeletonProps {
  /** Number of skeleton cards to render. */
  count?: number;
}

/**
 * A single skeleton card with pulsing animation.
 */
const SkeletonCard: React.FC = () => (
  <div
    className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 animate-pulse"
    data-testid="skeleton-card"
  >
    {/* Title */}
    <div className="h-5 bg-gray-200 rounded w-3/4 mb-3" />
    {/* Description line 1 */}
    <div className="h-3 bg-gray-200 rounded w-full mb-2" />
    {/* Description line 2 */}
    <div className="h-3 bg-gray-200 rounded w-2/3 mb-4" />
    {/* Footer */}
    <div className="pt-4 border-t border-gray-100 flex justify-between">
      <div className="h-3 bg-gray-200 rounded w-24" />
      <div className="h-5 w-5 bg-gray-200 rounded" />
    </div>
  </div>
);

/**
 * Grid of skeleton cards.
 */
export const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({ count = 6 }) => (
  <div
    className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
    data-testid="loading-skeleton"
  >
    {Array.from({ length: count }, (_, i) => (
      <SkeletonCard key={i} />
    ))}
  </div>
);
