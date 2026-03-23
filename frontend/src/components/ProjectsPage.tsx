/**
 * ProjectsPage – main page displaying the project grid, create modal, and states.
 */

import React, { useState } from 'react';
import { useProjects } from '../hooks/useProjects';
import { ProjectCard } from './ProjectCard';
import { CreateProjectModal } from './CreateProjectModal';
import { LoadingSkeleton } from './LoadingSkeleton';
import { EmptyState } from './EmptyState';

/**
 * Page component that fetches and displays all projects.
 */
export const ProjectsPage: React.FC = () => {
  const { projects, loading, error, addProject, removeProject } = useProjects();
  const [showModal, setShowModal] = useState(false);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage your projects and track progress
          </p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="inline-flex items-center px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-lg shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors duration-150"
          data-testid="create-project-btn"
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
          New Project
        </button>
      </div>

      {/* Error banner */}
      {error && (
        <div
          className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm"
          role="alert"
          data-testid="error-banner"
        >
          {error}
        </div>
      )}

      {/* Loading state */}
      {loading && <LoadingSkeleton count={6} />}

      {/* Empty state */}
      {!loading && projects.length === 0 && !error && (
        <EmptyState onCreateClick={() => setShowModal(true)} />
      )}

      {/* Project grid */}
      {!loading && projects.length > 0 && (
        <div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          data-testid="projects-grid"
        >
          {projects.map((project) => (
            <ProjectCard
              key={project.id}
              project={project}
              onDelete={removeProject}
            />
          ))}
        </div>
      )}

      {/* Create modal */}
      {showModal && (
        <CreateProjectModal
          onClose={() => setShowModal(false)}
          onCreate={addProject}
        />
      )}
    </div>
  );
};
