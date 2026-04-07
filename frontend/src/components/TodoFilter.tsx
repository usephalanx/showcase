import React from 'react';

export type FilterType = 'all' | 'active' | 'completed';

export interface TodoFilterProps {
  currentFilter: FilterType;
  onFilterChange: (filter: FilterType) => void;
  remainingCount: number;
}

const FILTERS: { label: string; value: FilterType }[] = [
  { label: 'All', value: 'all' },
  { label: 'Active', value: 'active' },
  { label: 'Completed', value: 'completed' },
];

const TodoFilter: React.FC<TodoFilterProps> = ({
  currentFilter,
  onFilterChange,
  remainingCount,
}) => {
  return (
    <div className="todo-filter">
      <span className="todo-filter-count" data-testid="remaining-count">
        {remainingCount} {remainingCount === 1 ? 'item' : 'items'} left
      </span>
      <div className="todo-filter-buttons" role="group" aria-label="Filter todos">
        {FILTERS.map(({ label, value }) => (
          <button
            key={value}
            type="button"
            className={`todo-filter-button${
              currentFilter === value ? ' todo-filter-button--active' : ''
            }`}
            aria-pressed={currentFilter === value}
            onClick={() => onFilterChange(value)}
          >
            {label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default TodoFilter;
