import React from 'react';
import { FilterType } from '../types/todo';

interface TodoFilterProps {
  currentFilter: FilterType;
  onFilterChange: (filter: FilterType) => void;
  remainingCount?: number;
}

const FILTERS: FilterType[] = ['all', 'active', 'completed'];

const TodoFilter: React.FC<TodoFilterProps> = ({
  currentFilter,
  onFilterChange,
  remainingCount = 0,
}) => {
  return (
    <div className="todo-filter">
      <span className="todo-filter-count">
        {remainingCount} {remainingCount === 1 ? 'item' : 'items'} left
      </span>
      <div className="todo-filter-buttons">
        {FILTERS.map((filter) => (
          <button
            key={filter}
            className={currentFilter === filter ? 'active' : ''}
            onClick={() => onFilterChange(filter)}
            aria-pressed={currentFilter === filter}
          >
            {filter.charAt(0).toUpperCase() + filter.slice(1)}
          </button>
        ))}
      </div>
    </div>
  );
};

export default TodoFilter;
