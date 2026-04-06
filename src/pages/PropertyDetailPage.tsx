import React from "react";
import { useParams, Link } from "react-router-dom";
import { MOCK_PROPERTIES } from "../data/mockProperties";

/**
 * Property detail page component.
 *
 * Displays comprehensive information about a single property listing,
 * including images, description, features, and agent contact information.
 * The property is identified by the `:id` route parameter.
 */
const PropertyDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const property = MOCK_PROPERTIES.find((p) => p.id === id);

  if (!property) {
    return (
      <main className="flex-1 flex flex-col items-center justify-center py-20 px-4">
        <h1 className="text-3xl font-bold text-slate-900 mb-4">
          Property Not Found
        </h1>
        <p className="text-slate-500 mb-8">
          The property you are looking for does not exist.
        </p>
        <Link
          to="/"
          className="text-blue-600 hover:text-blue-700 font-semibold"
        >
          &larr; Back to Listings
        </Link>
      </main>
    );
  }

  return (
    <main className="flex-1">
      {/* Navigation */}
      <div className="max-w-7xl mx-auto px-4 py-4">
        <Link
          to="/"
          className="text-blue-600 hover:text-blue-700 font-medium text-sm"
        >
          &larr; Back to Listings
        </Link>
      </div>

      {/* Image Gallery */}
      <section className="max-w-7xl mx-auto px-4 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {property.images.slice(0, 4).map((image, index) => (
            <div
              key={index}
              className={`overflow-hidden rounded-xl ${
                index === 0 ? "md:col-span-2 aspect-video" : "aspect-video"
              }`}
            >
              <img
                src={image}
                alt={`${property.title} — image ${index + 1}`}
                className="w-full h-full object-cover"
              />
            </div>
          ))}
        </div>
      </section>

      {/* Details */}
      <section className="max-w-7xl mx-auto px-4 pb-16">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            <div className="mb-4">
              <span className="inline-block bg-blue-100 text-blue-800 text-xs font-semibold px-3 py-1 rounded-full uppercase">
                {property.status}
              </span>
            </div>
            <h1 className="text-3xl md:text-4xl font-bold text-slate-900 mb-2">
              {property.title}
            </h1>
            <p className="text-slate-500 text-lg mb-4">
              {property.address}, {property.city}, {property.state}{" "}
              {property.zipCode}
            </p>
            <p className="text-3xl font-bold text-blue-600 mb-8">
              ${property.price.toLocaleString()}
            </p>

            {/* Stats */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
              <div className="bg-white rounded-lg p-4 shadow-sm text-center">
                <p className="text-2xl font-bold text-slate-900">
                  {property.bedrooms}
                </p>
                <p className="text-sm text-slate-500">Bedrooms</p>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm text-center">
                <p className="text-2xl font-bold text-slate-900">
                  {property.bathrooms}
                </p>
                <p className="text-sm text-slate-500">Bathrooms</p>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm text-center">
                <p className="text-2xl font-bold text-slate-900">
                  {property.squareFeet.toLocaleString()}
                </p>
                <p className="text-sm text-slate-500">Sq Ft</p>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm text-center">
                <p className="text-2xl font-bold text-slate-900">
                  {property.yearBuilt}
                </p>
                <p className="text-sm text-slate-500">Year Built</p>
              </div>
            </div>

            {/* Description */}
            <h2 className="text-xl font-semibold text-slate-900 mb-3">
              About This Property
            </h2>
            <p className="text-slate-600 leading-relaxed mb-8">
              {property.description}
            </p>

            {/* Features */}
            <h2 className="text-xl font-semibold text-slate-900 mb-3">
              Features
            </h2>
            <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-8">
              {property.features.map((feature, index) => (
                <li key={index} className="flex items-center text-slate-600">
                  <span className="w-2 h-2 bg-blue-600 rounded-full mr-3" />
                  {feature}
                </li>
              ))}
            </ul>
          </div>

          {/* Sidebar — Agent */}
          <aside className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm p-6 sticky top-8">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">
                Listed by
              </h3>
              <div className="flex items-center gap-4 mb-4">
                <img
                  src={property.agent.photo}
                  alt={property.agent.name}
                  className="w-14 h-14 rounded-full object-cover"
                />
                <div>
                  <p className="font-semibold text-slate-900">
                    {property.agent.name}
                  </p>
                  <p className="text-sm text-slate-500">
                    {property.agent.title}
                  </p>
                </div>
              </div>
              <p className="text-sm text-slate-600 mb-4">
                {property.agent.phone}
              </p>
              <Link
                to={`/contact?propertyId=${property.id}`}
                className="block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
              >
                Contact Agent
              </Link>
            </div>
          </aside>
        </div>
      </section>
    </main>
  );
};

export default PropertyDetailPage;
