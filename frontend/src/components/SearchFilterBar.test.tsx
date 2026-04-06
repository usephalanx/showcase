import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import SearchFilterBar, { SearchFilters } from './SearchFilterBar';

const defaultFilters: SearchFilters = {
  location: '',
  propertyType: '',
  minPrice: '',
  maxPrice: '',
  beds: '',
  baths: '',
};

describe('SearchFilterBar', () => {
  it('renders without crashing', () => {
    const { container } = render(
      <SearchFilterBar
        filters={defaultFilters}
        onFilterChange={() => {}}
        onSearch={() => {}}
      />,
    );
    expect(container).toBeTruthy();
  });

  it('renders all filter controls', () => {
    render(
      <SearchFilterBar
        filters={defaultFilters}
        onFilterChange={() => {}}
        onSearch={() => {}}
      />,
    );

    expect(screen.getByTestId('filter-location')).toBeInTheDocument();
    expect(screen.getByTestId('filter-property-type')).toBeInTheDocument();
    expect(screen.getByTestId('filter-min-price')).toBeInTheDocument();
    expect(screen.getByTestId('filter-max-price')).toBeInTheDocument();
    expect(screen.getByTestId('filter-beds')).toBeInTheDocument();
    expect(screen.getByTestId('filter-baths')).toBeInTheDocument();
    expect(screen.getByTestId('search-button')).toBeInTheDocument();
  });

  it('displays the current filter values', () => {
    const filters: SearchFilters = {
      location: 'Austin, TX',
      propertyType: 'house',
      minPrice: '200000',
      maxPrice: '500000',
      beds: '3',
      baths: '2',
    };

    render(
      <SearchFilterBar
        filters={filters}
        onFilterChange={() => {}}
        onSearch={() => {}}
      />,
    );

    expect(screen.getByTestId('filter-location')).toHaveValue('Austin, TX');
    expect(screen.getByTestId('filter-property-type')).toHaveValue('house');
    expect(screen.getByTestId('filter-min-price')).toHaveValue('200000');
    expect(screen.getByTestId('filter-max-price')).toHaveValue('500000');
    expect(screen.getByTestId('filter-beds')).toHaveValue('3');
    expect(screen.getByTestId('filter-baths')).toHaveValue('2');
  });

  it('calls onFilterChange when location input changes', async () => {
    const onFilterChange = vi.fn();
    const user = userEvent.setup();

    render(
      <SearchFilterBar
        filters={defaultFilters}
        onFilterChange={onFilterChange}
        onSearch={() => {}}
      />,
    );

    const locationInput = screen.getByTestId('filter-location');
    await user.type(locationInput, 'D');

    expect(onFilterChange).toHaveBeenCalledWith({
      ...defaultFilters,
      location: 'D',
    });
  });

  it('calls onFilterChange when property type changes', () => {
    const onFilterChange = vi.fn();

    render(
      <SearchFilterBar
        filters={defaultFilters}
        onFilterChange={onFilterChange}
        onSearch={() => {}}
      />,
    );

    fireEvent.change(screen.getByTestId('filter-property-type'), {
      target: { value: 'condo' },
    });

    expect(onFilterChange).toHaveBeenCalledWith({
      ...defaultFilters,
      propertyType: 'condo',
    });
  });

  it('calls onFilterChange when min price changes', () => {
    const onFilterChange = vi.fn();

    render(
      <SearchFilterBar
        filters={defaultFilters}
        onFilterChange={onFilterChange}
        onSearch={() => {}}
      />,
    );

    fireEvent.change(screen.getByTestId('filter-min-price'), {
      target: { value: '300000' },
    });

    expect(onFilterChange).toHaveBeenCalledWith({
      ...defaultFilters,
      minPrice: '300000',
    });
  });

  it('calls onFilterChange when max price changes', () => {
    const onFilterChange = vi.fn();

    render(
      <SearchFilterBar
        filters={defaultFilters}
        onFilterChange={onFilterChange}
        onSearch={() => {}}
      />,
    );

    fireEvent.change(screen.getByTestId('filter-max-price'), {
      target: { value: '750000' },
    });

    expect(onFilterChange).toHaveBeenCalledWith({
      ...defaultFilters,
      maxPrice: '750000',
    });
  });

  it('calls onFilterChange when beds changes', () => {
    const onFilterChange = vi.fn();

    render(
      <SearchFilterBar
        filters={defaultFilters}
        onFilterChange={onFilterChange}
        onSearch={() => {}}
      />,
    );

    fireEvent.change(screen.getByTestId('filter-beds'), {
      target: { value: '4' },
    });

    expect(onFilterChange).toHaveBeenCalledWith({
      ...defaultFilters,
      beds: '4',
    });
  });

  it('calls onFilterChange when baths changes', () => {
    const onFilterChange = vi.fn();

    render(
      <SearchFilterBar
        filters={defaultFilters}
        onFilterChange={onFilterChange}
        onSearch={() => {}}
      />,
    );

    fireEvent.change(screen.getByTestId('filter-baths'), {
      target: { value: '2' },
    });

    expect(onFilterChange).toHaveBeenCalledWith({
      ...defaultFilters,
      baths: '2',
    });
  });

  it('calls onSearch with current filters when form is submitted', () => {
    const onSearch = vi.fn();
    const filters: SearchFilters = {
      location: 'Denver',
      propertyType: 'apartment',
      minPrice: '100000',
      maxPrice: '500000',
      beds: '2',
      baths: '1',
    };

    render(
      <SearchFilterBar
        filters={filters}
        onFilterChange={() => {}}
        onSearch={onSearch}
      />,
    );

    fireEvent.click(screen.getByTestId('search-button'));

    expect(onSearch).toHaveBeenCalledTimes(1);
    expect(onSearch).toHaveBeenCalledWith(filters);
  });

  it('renders all property type options', () => {
    render(
      <SearchFilterBar
        filters={defaultFilters}
        onFilterChange={() => {}}
        onSearch={() => {}}
      />,
    );

    const select = screen.getByTestId('filter-property-type');
    const options = select.querySelectorAll('option');
    const labels = Array.from(options).map((o) => o.textContent);

    expect(labels).toEqual(['All', 'House', 'Apartment', 'Condo', 'Townhouse']);
  });

  it('renders bed/bath options with Any and numeric choices', () => {
    render(
      <SearchFilterBar
        filters={defaultFilters}
        onFilterChange={() => {}}
        onSearch={() => {}}
      />,
    );

    const bedsSelect = screen.getByTestId('filter-beds');
    const bedsOptions = bedsSelect.querySelectorAll('option');
    const bedsLabels = Array.from(bedsOptions).map((o) => o.textContent);

    expect(bedsLabels).toEqual(['Any', '1+', '2+', '3+', '4+', '5+']);
  });

  it('renders the search button with correct text', () => {
    render(
      <SearchFilterBar
        filters={defaultFilters}
        onFilterChange={() => {}}
        onSearch={() => {}}
      />,
    );

    expect(screen.getByTestId('search-button')).toHaveTextContent('Search');
  });

  it('has accessible labels for all inputs', () => {
    render(
      <SearchFilterBar
        filters={defaultFilters}
        onFilterChange={() => {}}
        onSearch={() => {}}
      />,
    );

    expect(screen.getByLabelText('Location')).toBeInTheDocument();
    expect(screen.getByLabelText('Type')).toBeInTheDocument();
    expect(screen.getByLabelText('Min Price')).toBeInTheDocument();
    expect(screen.getByLabelText('Max Price')).toBeInTheDocument();
    expect(screen.getByLabelText('Beds')).toBeInTheDocument();
    expect(screen.getByLabelText('Baths')).toBeInTheDocument();
  });
});
