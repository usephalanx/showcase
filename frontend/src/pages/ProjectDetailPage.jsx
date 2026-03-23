import React from 'react';
import { useParams, Link } from 'react-router-dom';

/**
 * ProjectDetailPage component.
 * Placeholder page for viewing a single project and its tasks.
 * Will be expanded with task board and detail views.
 */
export default function ProjectDetailPage() {
  const { id } = useParams();

  return (
    <div>
      <div className="mb-6">
        <Link
          to="/projects"
          className="text-sm text-primary transition-colors hover:text-blue-700"
        >
          &larr; Back to Projects
        </Link>
      </div>
      <div className="card">
        <h1 className="mb-4">Project #{id}</h1>
        <p className="text-gray-500">
          Project detail and task board will be displayed here. This page is
          under construction.
        </p>
      </div>
    </div>
  );
}
