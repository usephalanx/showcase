/**
 * EmptyState – displayed when no projects exist.
 */

import React from 'react';

interface EmptyStateProps {
  /** Callback when the user clicks "Create your first project". */
  onCreateClick: () => void;
}

/**
 * Empty state illustration and CTA.
 */
export const EmptyState: React.FC<EmptyStateProps> = ({ onCreateClick }) => (
  <div
    className="flex flex-col items-center justify-center py-16 px-4"
    data-testid="empty-state"
  >
    <div className="w-20 h-20 rounded-full bg-primary-50 flex items-center justify-center mb-6">
      <svg
        className="w-10 h-10 text-primary-500"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={1.5}
          d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"
        />
      </svg>
    </div>
    <h3 className="text-lg font-semibold text-gray-900 mb-2">No projects yet</h3>
    <p className="text-sm text-gray-500 mb-6 text-center max-w-sm">
      Get started by creating your first project. You can organize tasks,
      track progress, and manage your work.
    </p>
    <button
      onClick={onCreateClick}
      className="inline-flex items-center px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-lg shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors duration-150"
      data-testid="empty-create-btn"
    >
      <svg
        className="w-5 h-5 mr-2 -ml-1"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M12 4v16m8-8H4"
        />
      </svg>
      Create your first project
    </button>
  </div>
);
