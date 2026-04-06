import React, { useState, useMemo, useCallback, useRef } from 'react';
import { Link } from 'react-router-dom';
import { MOCK_PROPERTIES } from '../data/mockProperties';
import { MOCK_AGENTS } from '../data/mockAgents';
import { MOCK_NEIGHBORHOODS } from '../data/mockNeighborhoods';
import { Property, PropertyType } from '../types/models';

/* ------------------------------------------------------------------ */
/*  Filter state type                                                  */
/* ------------------------------------------------------------------ */
interface Filters {
  location: string;
  propertyType: PropertyType | '';
  minPrice: number;
  maxPrice: number;
  minBeds: number;
  minBaths: number;
}

const DEFAULT_FILTERS: Filters = {
  location: '',
  propertyType: '',
  minPrice: 0,
  maxPrice: 10000000,
  minBeds: 0,
  minBaths: 0,
};

/* ------------------------------------------------------------------ */
/*  Smooth-scroll helper                                               */
/* ------------------------------------------------------------------ */
const scrollTo = (ref: React.RefObject<HTMLElement | null>) => {
  ref.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
};

/* ------------------------------------------------------------------ */
/*  HomePage                                                           */
/* ------------------------------------------------------------------ */
const HomePage: React.FC = () => {
  const [filters, setFilters] = useState<Filters>(DEFAULT_FILTERS);

  /* section refs for smooth scrolling */
  const featuredRef = useRef<HTMLElement>(null);
  const neighborhoodRef = useRef<HTMLElement>(null);
  const agentsRef = useRef<HTMLElement>(null);

  /* ---- filter logic ------------------------------------------------ */
  const filteredProperties: Property[] = useMemo(() => {
    return MOCK_PROPERTIES.filter((p) => {
      if (
        filters.location &&
        !p.city.toLowerCase().includes(filters.location.toLowerCase()) &&
        !p.state.toLowerCase().includes(filters.location.toLowerCase()) &&
        !p.address.toLowerCase().includes(filters.location.toLowerCase())
      ) {
        return false;
      }
      if (filters.propertyType && p.propertyType !== filters.propertyType) return false;
      if (p.price < filters.minPrice) return false;
      if (p.price > filters.maxPrice) return false;
      if (p.bedrooms < filters.minBeds) return false;
      if (p.bathrooms < filters.minBaths) return false;
      return true;
    });
  }, [filters]);

  const hasActiveFilters = useMemo(
    () =>
      filters.location !== '' ||
      filters.propertyType !== '' ||
      filters.minPrice !== 0 ||
      filters.maxPrice !== 10000000 ||
      filters.minBeds !== 0 ||
      filters.minBaths !== 0,
    [filters],
  );

  const updateFilter = useCallback(
    <K extends keyof Filters>(key: K, value: Filters[K]) => {
      setFilters((prev) => ({ ...prev, [key]: value }));
    },
    [],
  );

  const resetFilters = useCallback(() => setFilters(DEFAULT_FILTERS), []);

  /* ---- render ------------------------------------------------------ */
  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      {/* ===================== HEADER ===================== */}
      <header className="sticky top-0 z-50 bg-white/95 backdrop-blur shadow-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between px-4 py-4">
          <Link to="/" className="text-2xl font-bold text-blue-600 tracking-tight">
            Premier<span className="text-slate-900">Realty</span>
          </Link>
          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-700">
            <button onClick={() => scrollTo(featuredRef)} className="hover:text-blue-600 transition-colors">Properties</button>
            <button onClick={() => scrollTo(neighborhoodRef)} className="hover:text-blue-600 transition-colors">Neighborhoods</button>
            <button onClick={() => scrollTo(agentsRef)} className="hover:text-blue-600 transition-colors">Agents</button>
            <Link to="/contact" className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg transition-colors">Contact Us</Link>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        {/* ===================== HERO SECTION ===================== */}
        <section className="relative bg-gradient-to-br from-slate-900 via-slate-800 to-blue-900 text-white pt-20 pb-32 px-4 text-center overflow-hidden">
          <div className="absolute inset-0 opacity-20 bg-[url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1920&h=1080&fit=crop')] bg-cover bg-center" />
          <div className="relative z-10 max-w-3xl mx-auto">
            <h1 className="text-4xl md:text-6xl font-extrabold mb-5 leading-tight">
              Find Your Dream Home
            </h1>
            <p className="text-lg md:text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
              Browse luxury real estate listings, connect with top agents, and explore the best neighborhoods.
            </p>
            <button
              onClick={() => scrollTo(featuredRef)}
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors"
            >
              Explore Properties
            </button>
          </div>
        </section>

        {/* ===================== SEARCH / FILTER BAR ===================== */}
        <section className="relative z-20 -mt-12 max-w-6xl mx-auto px-4">
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
              {/* Location */}
              <div className="lg:col-span-2">
                <label className="block text-xs font-semibold text-slate-500 mb-1">Location</label>
                <input
                  type="text"
                  value={filters.location}
                  onChange={(e) => updateFilter('location', e.target.value)}
                  placeholder="City, state, or address"
                  className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              {/* Property Type */}
              <div>
                <label className="block text-xs font-semibold text-slate-500 mb-1">Type</label>
                <select
                  value={filters.propertyType}
                  onChange={(e) => updateFilter('propertyType', e.target.value as PropertyType | '')}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
                >
                  <option value="">All Types</option>
                  <option value="house">House</option>
                  <option value="condo">Condo</option>
                  <option value="townhouse">Townhouse</option>
                  <option value="apartment">Apartment</option>
                  <option value="land">Land</option>
                </select>
              </div>

              {/* Price Range */}
              <div>
                <label className="block text-xs font-semibold text-slate-500 mb-1">Max Price</label>
                <select
                  value={filters.maxPrice}
                  onChange={(e) => updateFilter('maxPrice', Number(e.target.value))}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
                >
                  <option value={10000000}>Any</option>
                  <option value={300000}>$300k</option>
                  <option value={500000}>$500k</option>
                  <option value={750000}>$750k</option>
                  <option value={1000000}>$1M</option>
                  <option value={2000000}>$2M</option>
                </select>
              </div>

              {/* Beds */}
              <div>
                <label className="block text-xs font-semibold text-slate-500 mb-1">Beds</label>
                <select
                  value={filters.minBeds}
                  onChange={(e) => updateFilter('minBeds', Number(e.target.value))}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
                >
                  <option value={0}>Any</option>
                  <option value={1}>1+</option>
                  <option value={2}>2+</option>
                  <option value={3}>3+</option>
                  <option value={4}>4+</option>
                  <option value={5}>5+</option>
                </select>
              </div>

              {/* Baths */}
              <div>
                <label className="block text-xs font-semibold text-slate-500 mb-1">Baths</label>
                <select
                  value={filters.minBaths}
                  onChange={(e) => updateFilter('minBaths', Number(e.target.value))}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
                >
                  <option value={0}>Any</option>
                  <option value={1}>1+</option>
                  <option value={2}>2+</option>
                  <option value={3}>3+</option>
                  <option value={4}>4+</option>
                </select>
              </div>
            </div>

            {hasActiveFilters && (
              <div className="mt-3 flex items-center justify-between">
                <p className="text-sm text-slate-500">
                  {filteredProperties.length} {filteredProperties.length === 1 ? 'property' : 'properties'} found
                </p>
                <button
                  onClick={resetFilters}
                  className="text-sm text-blue-600 hover:text-blue-800 font-medium transition-colors"
                >
                  Reset Filters
                </button>
              </div>
            )}
          </div>
        </section>

        {/* ===================== FEATURED / FILTERED PROPERTIES ===================== */}
        <section ref={featuredRef} className="max-w-7xl mx-auto py-16 px-4 scroll-mt-24">
          <h2 className="text-3xl font-bold text-slate-900 mb-2">
            {hasActiveFilters ? 'Search Results' : 'Featured Properties'}
          </h2>
          <p className="text-slate-500 mb-8">
            {hasActiveFilters
              ? `Showing ${filteredProperties.length} matching properties`
              : 'Hand-picked homes you\'ll love'}
          </p>

          {filteredProperties.length === 0 ? (
            <div className="text-center py-16 bg-white rounded-xl shadow-sm">
              <p className="text-slate-400 text-lg mb-4">No properties match your filters.</p>
              <button onClick={resetFilters} className="text-blue-600 hover:text-blue-800 font-medium">
                Clear all filters
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {(hasActiveFilters ? filteredProperties : filteredProperties.slice(0, 6)).map((property) => (
                <Link
                  key={property.id}
                  to={`/property/${property.slug}`}
                  className="group block bg-white rounded-xl shadow-sm hover:shadow-lg transition-shadow overflow-hidden"
                >
                  <div className="aspect-video overflow-hidden relative">
                    <img
                      src={property.images[0]}
                      alt={property.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      loading="lazy"
                    />
                    <span className="absolute top-3 left-3 bg-blue-600 text-white text-xs font-semibold px-2.5 py-1 rounded-full capitalize">
                      {property.status.replace('-', ' ')}
                    </span>
                  </div>
                  <div className="p-5">
                    <h3 className="text-lg font-semibold text-slate-900 mb-1 group-hover:text-blue-600 transition-colors">
                      {property.title}
                    </h3>
                    <p className="text-slate-500 text-sm mb-2">
                      {property.address}, {property.city}, {property.state}
                    </p>
                    <p className="text-2xl font-bold text-blue-600">
                      ${property.price.toLocaleString()}
                    </p>
                    <div className="flex gap-4 mt-3 text-sm text-slate-600">
                      <span>{property.bedrooms} bd</span>
                      <span>{property.bathrooms} ba</span>
                      <span>{property.squareFeet.toLocaleString()} sqft</span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </section>

        {/* ===================== NEIGHBORHOOD HIGHLIGHTS ===================== */}
        <section ref={neighborhoodRef} className="bg-white py-16 px-4 scroll-mt-24">
          <div className="max-w-7xl mx-auto">
            <h2 className="text-3xl font-bold text-slate-900 mb-2">Explore Neighborhoods</h2>
            <p className="text-slate-500 mb-10">Discover the communities that make each area special</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {MOCK_NEIGHBORHOODS.map((hood) => (
                <div
                  key={hood.id}
                  className="group relative rounded-xl overflow-hidden shadow-sm hover:shadow-lg transition-shadow cursor-pointer"
                  onClick={() => {
                    updateFilter('location', hood.city);
                    scrollTo(featuredRef);
                  }}
                >
                  <div className="aspect-[4/5] overflow-hidden">
                    <img
                      src={hood.image}
                      alt={hood.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      loading="lazy"
                    />
                  </div>
                  <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
                  <div className="absolute bottom-0 left-0 right-0 p-5 text-white">
                    <h3 className="text-xl font-bold mb-1">{hood.name}</h3>
                    <p className="text-sm text-slate-200 mb-2">{hood.city}, {hood.state}</p>
                    <div className="flex items-center gap-3 text-xs">
                      <span className="bg-white/20 backdrop-blur rounded-full px-2.5 py-1">
                        Avg ${(hood.averagePrice / 1000).toFixed(0)}k
                      </span>
                      <span className="bg-white/20 backdrop-blur rounded-full px-2.5 py-1">
                        Walk {hood.walkScore}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ===================== AGENTS SECTION ===================== */}
        <section ref={agentsRef} className="max-w-7xl mx-auto py-16 px-4 scroll-mt-24">
          <h2 className="text-3xl font-bold text-slate-900 mb-2">Meet Our Agents</h2>
          <p className="text-slate-500 mb-10">Experienced professionals ready to help you</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {MOCK_AGENTS.map((agent) => (
              <div key={agent.id} className="bg-white rounded-xl shadow-sm hover:shadow-lg transition-shadow p-6 text-center">
                <img
                  src={agent.photo}
                  alt={agent.name}
                  className="w-24 h-24 rounded-full mx-auto mb-4 object-cover ring-4 ring-slate-100"
                  loading="lazy"
                />
                <h3 className="font-semibold text-slate-900 text-lg">{agent.name}</h3>
                <p className="text-sm text-blue-600 mb-3">{agent.title}</p>
                <p className="text-sm text-slate-500 mb-4 line-clamp-3">{agent.bio}</p>
                <div className="flex justify-center gap-3 text-xs text-slate-600">
                  <span className="bg-slate-100 rounded-full px-3 py-1">
                    ★ {agent.rating}
                  </span>
                  <span className="bg-slate-100 rounded-full px-3 py-1">
                    {agent.propertiesCount} listings
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>

      {/* ===================== FOOTER ===================== */}
      <footer className="bg-slate-900 text-slate-400 py-12 px-4">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <p className="text-xl font-bold text-white mb-3">
              Premier<span className="text-blue-400">Realty</span>
            </p>
            <p className="text-sm leading-relaxed">
              Your trusted partner in finding the perfect home. Premium service, exceptional properties.
            </p>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-3">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li><button onClick={() => scrollTo(featuredRef)} className="hover:text-white transition-colors">Properties</button></li>
              <li><button onClick={() => scrollTo(neighborhoodRef)} className="hover:text-white transition-colors">Neighborhoods</button></li>
              <li><button onClick={() => scrollTo(agentsRef)} className="hover:text-white transition-colors">Our Agents</button></li>
              <li><Link to="/contact" className="hover:text-white transition-colors">Contact</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-3">Property Types</h4>
            <ul className="space-y-2 text-sm">
              {['Houses', 'Condos', 'Townhouses', 'Apartments'].map((t) => (
                <li key={t}>
                  <button
                    onClick={() => {
                      updateFilter('propertyType', t.slice(0, -1).toLowerCase() as PropertyType);
                      scrollTo(featuredRef);
                    }}
                    className="hover:text-white transition-colors"
                  >
                    {t}
                  </button>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-3">Contact</h4>
            <ul className="space-y-2 text-sm">
              <li>123 Realty Blvd, Suite 100</li>
              <li>Austin, TX 73301</li>
              <li>info@premierealty.com</li>
              <li>(512) 555-0000</li>
            </ul>
          </div>
        </div>
        <div className="max-w-7xl mx-auto mt-10 pt-6 border-t border-slate-800 text-center text-sm">
          © {new Date().getFullYear()} PremierRealty. All rights reserved.
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
