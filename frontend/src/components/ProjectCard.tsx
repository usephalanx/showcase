/**
 * ProjectCard – renders a single project in the grid with name, description,
 * date, and delete button with confirmation.
 */

import React, { useState } from 'react';
import type { Project } from '../types';

interface ProjectCardProps {
  /** The project to display. */
  project: Project;
  /** Callback to delete the project by its ID. */
  onDelete: (id: number) => Promise<void>;
}

/**
 * Format an ISO date string to a human-readable format.
 */
function formatDate(isoString: string): string {
  const date = new Date(isoString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

/**
 * Truncate a string to the given max length, appending "…" if truncated.
 */
function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength).trimEnd() + '…';
}

/**
 * Card component displaying a project summary.
 */
export const ProjectCard: React.FC<ProjectCardProps> = ({ project, onDelete }) => {
  const [confirming, setConfirming] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleDeleteClick = () => {
    setConfirming(true);
  };

  const handleConfirm = async () => {
    setDeleting(true);
    try {
      await onDelete(project.id);
    } finally {
      setDeleting(false);
      setConfirming(false);
    }
  };

  const handleCancel = () => {
    setConfirming(false);
  };

  return (
    <div
      className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-gray-300 transition-all duration-200 flex flex-col"
      data-testid={`project-card-${project.id}`}
    >
      {/* Title */}
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{project.name}</h3>

      {/* Description */}
      <p className="text-sm text-gray-500 mb-4 flex-1 min-h-[2.5rem]">
        {project.description ? truncate(project.description, 120) : (
          <span className="italic text-gray-400">No description</span>
        )}
      </p>

      {/* Footer */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <span className="text-xs text-gray-400">
          Created {formatDate(project.created_at)}
        </span>

        {!confirming ? (
          <button
            onClick={handleDeleteClick}
            className="text-sm text-gray-400 hover:text-red-600 transition-colors duration-150 p-1"
            data-testid={`delete-btn-${project.id}`}
            aria-label={`Delete project ${project.name}`}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        ) : (
          <div className="flex items-center gap-2">
            <span className="text-xs text-red-600 font-medium">Delete?</span>
            <button
              onClick={handleConfirm}
              disabled={deleting}
              className="text-xs px-2 py-1 bg-red-600 text-white rounded hover:bg-red-700 disabled:opacity-50 transition-colors duration-150"
              data-testid={`confirm-delete-btn-${project.id}`}
            >
              {deleting ? '…' : 'Yes'}
            </button>
            <button
              onClick={handleCancel}
              disabled={deleting}
              className="text-xs px-2 py-1 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 disabled:opacity-50 transition-colors duration-150"
              data-testid={`cancel-delete-btn-${project.id}`}
            >
              No
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
