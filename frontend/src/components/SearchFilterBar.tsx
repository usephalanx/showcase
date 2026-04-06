import React from 'react';

export interface SearchFilters {
  location: string;
  propertyType: string;
  minPrice: string;
  maxPrice: string;
  beds: string;
  baths: string;
}

export interface SearchFilterBarProps {
  filters: SearchFilters;
  onFilterChange: (filters: SearchFilters) => void;
  onSearch: (filters: SearchFilters) => void;
}

const PROPERTY_TYPES = [
  { value: '', label: 'All' },
  { value: 'house', label: 'House' },
  { value: 'apartment', label: 'Apartment' },
  { value: 'condo', label: 'Condo' },
  { value: 'townhouse', label: 'Townhouse' },
];

const PRICE_OPTIONS = [
  { value: '', label: 'No Min' },
  { value: '50000', label: '$50,000' },
  { value: '100000', label: '$100,000' },
  { value: '200000', label: '$200,000' },
  { value: '300000', label: '$300,000' },
  { value: '400000', label: '$400,000' },
  { value: '500000', label: '$500,000' },
  { value: '750000', label: '$750,000' },
  { value: '1000000', label: '$1,000,000' },
  { value: '1500000', label: '$1,500,000' },
  { value: '2000000', label: '$2,000,000' },
];

const MAX_PRICE_OPTIONS = [
  { value: '', label: 'No Max' },
  ...PRICE_OPTIONS.slice(1),
];

const BED_BATH_OPTIONS = [
  { value: '', label: 'Any' },
  { value: '1', label: '1+' },
  { value: '2', label: '2+' },
  { value: '3', label: '3+' },
  { value: '4', label: '4+' },
  { value: '5', label: '5+' },
];

const selectClass =
  'w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-700 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500';

const SearchFilterBar: React.FC<SearchFilterBarProps> = ({
  filters,
  onFilterChange,
  onSearch,
}) => {
  const handleChange = (
    field: keyof SearchFilters,
    value: string,
  ) => {
    onFilterChange({ ...filters, [field]: value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(filters);
  };

  return (
    <form
      onSubmit={handleSubmit}
      data-testid="search-filter-bar"
      className="w-full rounded-xl bg-white p-4 shadow-lg md:p-6"
    >
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 xl:grid-cols-7 items-end">
        {/* Location */}
        <div className="sm:col-span-2 md:col-span-1 lg:col-span-2 xl:col-span-2">
          <label htmlFor="sfb-location" className="mb-1 block text-xs font-semibold uppercase tracking-wide text-gray-500">
            Location
          </label>
          <input
            id="sfb-location"
            type="text"
            placeholder="City, ZIP, or Address"
            value={filters.location}
            onChange={(e) => handleChange('location', e.target.value)}
            className="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-700 shadow-sm placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            data-testid="filter-location"
          />
        </div>

        {/* Property Type */}
        <div>
          <label htmlFor="sfb-property-type" className="mb-1 block text-xs font-semibold uppercase tracking-wide text-gray-500">
            Type
          </label>
          <select
            id="sfb-property-type"
            value={filters.propertyType}
            onChange={(e) => handleChange('propertyType', e.target.value)}
            className={selectClass}
            data-testid="filter-property-type"
          >
            {PROPERTY_TYPES.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>

        {/* Min Price */}
        <div>
          <label htmlFor="sfb-min-price" className="mb-1 block text-xs font-semibold uppercase tracking-wide text-gray-500">
            Min Price
          </label>
          <select
            id="sfb-min-price"
            value={filters.minPrice}
            onChange={(e) => handleChange('minPrice', e.target.value)}
            className={selectClass}
            data-testid="filter-min-price"
          >
            {PRICE_OPTIONS.map((opt) => (
              <option key={`min-${opt.value}`} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>

        {/* Max Price */}
        <div>
          <label htmlFor="sfb-max-price" className="mb-1 block text-xs font-semibold uppercase tracking-wide text-gray-500">
            Max Price
          </label>
          <select
            id="sfb-max-price"
            value={filters.maxPrice}
            onChange={(e) => handleChange('maxPrice', e.target.value)}
            className={selectClass}
            data-testid="filter-max-price"
          >
            {MAX_PRICE_OPTIONS.map((opt) => (
              <option key={`max-${opt.value}`} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>

        {/* Beds & Baths row on small screens, individual on large */}
        <div className="grid grid-cols-2 gap-3 sm:col-span-2 md:col-span-1 lg:col-span-1 xl:col-span-1">
          <div>
            <label htmlFor="sfb-beds" className="mb-1 block text-xs font-semibold uppercase tracking-wide text-gray-500">
              Beds
            </label>
            <select
              id="sfb-beds"
              value={filters.beds}
              onChange={(e) => handleChange('beds', e.target.value)}
              className={selectClass}
              data-testid="filter-beds"
            >
              {BED_BATH_OPTIONS.map((opt) => (
                <option key={`beds-${opt.value}`} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="sfb-baths" className="mb-1 block text-xs font-semibold uppercase tracking-wide text-gray-500">
              Baths
            </label>
            <select
              id="sfb-baths"
              value={filters.baths}
              onChange={(e) => handleChange('baths', e.target.value)}
              className={selectClass}
              data-testid="filter-baths"
            >
              {BED_BATH_OPTIONS.map((opt) => (
                <option key={`baths-${opt.value}`} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Search Button */}
        <div className="flex items-end sm:col-span-2 md:col-span-3 lg:col-span-1 xl:col-span-1">
          <button
            type="submit"
            className="w-full rounded-md bg-blue-600 px-6 py-2 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            data-testid="search-button"
          >
            Search
          </button>
        </div>
      </div>
    </form>
  );
};

export default SearchFilterBar;
