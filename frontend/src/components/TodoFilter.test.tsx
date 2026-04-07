import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TodoFilter, { FilterType } from './TodoFilter';

const defaultProps = {
  currentFilter: 'all' as FilterType,
  onFilterChange: vi.fn(),
  remainingCount: 3,
};

describe('TodoFilter', () => {
  it('renders all three filter buttons', () => {
    render(<TodoFilter {...defaultProps} />);

    expect(screen.getByRole('button', { name: 'All' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Active' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Completed' })).toBeInTheDocument();
  });

  it('highlights the active filter button', () => {
    render(<TodoFilter {...defaultProps} currentFilter="active" />);

    const allButton = screen.getByRole('button', { name: 'All' });
    const activeButton = screen.getByRole('button', { name: 'Active' });
    const completedButton = screen.getByRole('button', { name: 'Completed' });

    expect(activeButton).toHaveAttribute('aria-pressed', 'true');
    expect(activeButton.className).toContain('todo-filter-button--active');

    expect(allButton).toHaveAttribute('aria-pressed', 'false');
    expect(allButton.className).not.toContain('todo-filter-button--active');

    expect(completedButton).toHaveAttribute('aria-pressed', 'false');
    expect(completedButton.className).not.toContain('todo-filter-button--active');
  });

  it('calls onFilterChange when a filter button is clicked', async () => {
    const onFilterChange = vi.fn();
    const user = userEvent.setup();

    render(<TodoFilter {...defaultProps} onFilterChange={onFilterChange} />);

    await user.click(screen.getByRole('button', { name: 'Completed' }));
    expect(onFilterChange).toHaveBeenCalledTimes(1);
    expect(onFilterChange).toHaveBeenCalledWith('completed');

    await user.click(screen.getByRole('button', { name: 'Active' }));
    expect(onFilterChange).toHaveBeenCalledTimes(2);
    expect(onFilterChange).toHaveBeenCalledWith('active');

    await user.click(screen.getByRole('button', { name: 'All' }));
    expect(onFilterChange).toHaveBeenCalledTimes(3);
    expect(onFilterChange).toHaveBeenCalledWith('all');
  });

  it('displays the remaining count correctly', () => {
    render(<TodoFilter {...defaultProps} remainingCount={5} />);
    expect(screen.getByTestId('remaining-count')).toHaveTextContent('5 items left');
  });

  it('uses singular "item" when remainingCount is 1', () => {
    render(<TodoFilter {...defaultProps} remainingCount={1} />);
    expect(screen.getByTestId('remaining-count')).toHaveTextContent('1 item left');
  });

  it('handles zero remaining count', () => {
    render(<TodoFilter {...defaultProps} remainingCount={0} />);
    expect(screen.getByTestId('remaining-count')).toHaveTextContent('0 items left');
  });

  it('renders without crashing with default props', () => {
    const { container } = render(<TodoFilter {...defaultProps} />);
    expect(container.querySelector('.todo-filter')).toBeInTheDocument();
  });
});
