import React from "react";
import { Link } from "react-router-dom";
import { getFeaturedProperties } from "../data/mockProperties";

/**
 * Home page component.
 *
 * Displays a hero section and a grid of featured property listings.
 * Serves as the landing page for the real estate website.
 */
const HomePage: React.FC = () => {
  const featuredProperties = getFeaturedProperties();

  return (
    <main className="flex-1">
      {/* Hero Section */}
      <section className="bg-slate-900 text-white py-20 px-4 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          Find Your Dream Home
        </h1>
        <p className="text-lg md:text-xl text-slate-300 max-w-2xl mx-auto mb-8">
          Browse luxury real estate listings, connect with top agents, and
          explore the best neighborhoods.
        </p>
        <Link
          to="/contact"
          className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors"
        >
          Get in Touch
        </Link>
      </section>

      {/* Featured Properties */}
      <section className="max-w-7xl mx-auto py-16 px-4">
        <h2 className="text-3xl font-bold text-slate-900 mb-8">
          Featured Properties
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {featuredProperties.map((property) => (
            <Link
              key={property.id}
              to={`/property/${property.id}`}
              className="group block bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow overflow-hidden"
            >
              <div className="aspect-video overflow-hidden">
                <img
                  src={property.images[0]}
                  alt={property.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
              </div>
              <div className="p-5">
                <h3 className="text-xl font-semibold text-slate-900 mb-1">
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
      </section>
    </main>
  );
};

export default HomePage;
