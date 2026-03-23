/**
 * Tests for the ProjectsPage, ProjectCard, CreateProjectModal, and related
 * components.
 */

import React from 'react';
import { describe, it, expect, vi, beforeEach, type Mock } from 'vitest';
import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ProjectsPage } from '../components/ProjectsPage';
import * as projectsApi from '../api/projects';
import type { Project } from '../types';

// Mock the API module
vi.mock('../api/projects');

const mockProjects: Project[] = [
  {
    id: 1,
    name: 'Project Alpha',
    description: 'Description for Alpha',
    created_at: '2024-01-15T10:00:00',
  },
  {
    id: 2,
    name: 'Project Beta',
    description: null,
    created_at: '2024-02-20T12:00:00',
  },
  {
    id: 3,
    name: 'Project Gamma',
    description:
      'A very long description that should be truncated because it exceeds the maximum display length set in the card component and we want to ensure truncation works properly.',
    created_at: '2024-03-10T08:30:00',
  },
];

beforeEach(() => {
  vi.clearAllMocks();
});

describe('ProjectsPage', () => {
  it('shows loading skeleton initially', () => {
    // Never resolve the fetch to keep loading state
    (projectsApi.fetchProjects as Mock).mockReturnValue(new Promise(() => {}));
    render(<ProjectsPage />);
    expect(screen.getByTestId('loading-skeleton')).toBeInTheDocument();
  });

  it('shows empty state when no projects exist', async () => {
    (projectsApi.fetchProjects as Mock).mockResolvedValue([]);
    render(<ProjectsPage />);
    await waitFor(() => {
      expect(screen.getByTestId('empty-state')).toBeInTheDocument();
    });
    expect(screen.getByText('No projects yet')).toBeInTheDocument();
  });

  it('renders project cards in a grid', async () => {
    (projectsApi.fetchProjects as Mock).mockResolvedValue(mockProjects);
    render(<ProjectsPage />);
    await waitFor(() => {
      expect(screen.getByTestId('projects-grid')).toBeInTheDocument();
    });
    expect(screen.getByText('Project Alpha')).toBeInTheDocument();
    expect(screen.getByText('Project Beta')).toBeInTheDocument();
    expect(screen.getByText('Project Gamma')).toBeInTheDocument();
  });

  it('shows error banner on fetch failure', async () => {
    (projectsApi.fetchProjects as Mock).mockRejectedValue(
      new Error('Network error')
    );
    render(<ProjectsPage />);
    await waitFor(() => {
      expect(screen.getByTestId('error-banner')).toBeInTheDocument();
    });
    expect(screen.getByText('Network error')).toBeInTheDocument();
  });

  it('truncates long descriptions', async () => {
    (projectsApi.fetchProjects as Mock).mockResolvedValue(mockProjects);
    render(<ProjectsPage />);
    await waitFor(() => {
      expect(screen.getByTestId('projects-grid')).toBeInTheDocument();
    });
    // The long description for Project Gamma should be truncated
    const card = screen.getByTestId('project-card-3');
    const descriptionText = card.querySelector('p')!.textContent!;
    expect(descriptionText.endsWith('…')).toBe(true);
    expect(descriptionText.length).toBeLessThanOrEqual(125); // 120 chars + "…"
  });

  it('shows "No description" for null descriptions', async () => {
    (projectsApi.fetchProjects as Mock).mockResolvedValue(mockProjects);
    render(<ProjectsPage />);
    await waitFor(() => {
      expect(screen.getByTestId('projects-grid')).toBeInTheDocument();
    });
    const card = screen.getByTestId('project-card-2');
    expect(within(card).getByText('No description')).toBeInTheDocument();
  });
});

describe('CreateProjectModal', () => {
  it('opens modal and creates project', async () => {
    const user = userEvent.setup();
    const newProject: Project = {
      id: 4,
      name: 'New Project',
      description: 'A description',
      created_at: '2024-04-01T00:00:00',
    };
    (projectsApi.fetchProjects as Mock).mockResolvedValue([]);
    (projectsApi.createProject as Mock).mockResolvedValue(newProject);

    render(<ProjectsPage />);
    await waitFor(() => {
      expect(screen.getByTestId('empty-state')).toBeInTheDocument();
    });

    // Click New Project button
    await user.click(screen.getByTestId('create-project-btn'));
    expect(screen.getByTestId('create-project-modal')).toBeInTheDocument();

    // Fill form
    await user.type(screen.getByTestId('project-name-input'), 'New Project');
    await user.type(
      screen.getByTestId('project-description-input'),
      'A description'
    );

    // Submit
    await user.click(screen.getByTestId('modal-submit-btn'));

    await waitFor(() => {
      expect(projectsApi.createProject).toHaveBeenCalledWith({
        name: 'New Project',
        description: 'A description',
      });
    });

    // Modal should close and project should appear
    await waitFor(() => {
      expect(screen.queryByTestId('create-project-modal')).not.toBeInTheDocument();
    });
    expect(screen.getByText('New Project')).toBeInTheDocument();
  });

  it('shows validation error when name is empty', async () => {
    const user = userEvent.setup();
    (projectsApi.fetchProjects as Mock).mockResolvedValue([]);

    render(<ProjectsPage />);
    await waitFor(() => {
      expect(screen.getByTestId('empty-state')).toBeInTheDocument();
    });

    await user.click(screen.getByTestId('create-project-btn'));
    // Submit without entering name
    await user.click(screen.getByTestId('modal-submit-btn'));

    expect(screen.getByTestId('name-error')).toBeInTheDocument();
    expect(screen.getByText('Project name is required')).toBeInTheDocument();
    expect(projectsApi.createProject).not.toHaveBeenCalled();
  });

  it('closes modal on cancel', async () => {
    const user = userEvent.setup();
    (projectsApi.fetchProjects as Mock).mockResolvedValue([]);

    render(<ProjectsPage />);
    await waitFor(() => {
      expect(screen.getByTestId('empty-state')).toBeInTheDocument();
    });

    await user.click(screen.getByTestId('create-project-btn'));
    expect(screen.getByTestId('create-project-modal')).toBeInTheDocument();

    await user.click(screen.getByTestId('modal-cancel-btn'));
    await waitFor(() => {
      expect(screen.queryByTestId('create-project-modal')).not.toBeInTheDocument();
    });
  });
});

describe('ProjectCard delete', () => {
  it('shows confirmation and deletes on confirm', async () => {
    const user = userEvent.setup();
    (projectsApi.fetchProjects as Mock).mockResolvedValue([mockProjects[0]]);
    (projectsApi.deleteProject as Mock).mockResolvedValue(undefined);

    render(<ProjectsPage />);
    await waitFor(() => {
      expect(screen.getByTestId('projects-grid')).toBeInTheDocument();
    });

    // Click delete icon
    await user.click(screen.getByTestId('delete-btn-1'));
    // Confirmation should appear
    expect(screen.getByText('Delete?')).toBeInTheDocument();
    expect(screen.getByTestId('confirm-delete-btn-1')).toBeInTheDocument();
    expect(screen.getByTestId('cancel-delete-btn-1')).toBeInTheDocument();

    // Confirm delete
    await user.click(screen.getByTestId('confirm-delete-btn-1'));

    await waitFor(() => {
      expect(projectsApi.deleteProject).toHaveBeenCalledWith(1);
    });

    // Card should be removed
    await waitFor(() => {
      expect(screen.queryByText('Project Alpha')).not.toBeInTheDocument();
    });
  });

  it('cancels delete on No click', async () => {
    const user = userEvent.setup();
    (projectsApi.fetchProjects as Mock).mockResolvedValue([mockProjects[0]]);

    render(<ProjectsPage />);
    await waitFor(() => {
      expect(screen.getByTestId('projects-grid')).toBeInTheDocument();
    });

    await user.click(screen.getByTestId('delete-btn-1'));
    expect(screen.getByText('Delete?')).toBeInTheDocument();

    await user.click(screen.getByTestId('cancel-delete-btn-1'));
    // Confirmation should disappear but card remains
    expect(screen.queryByText('Delete?')).not.toBeInTheDocument();
    expect(screen.getByText('Project Alpha')).toBeInTheDocument();
    expect(projectsApi.deleteProject).not.toHaveBeenCalled();
  });
});
