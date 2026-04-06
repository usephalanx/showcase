import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { MOCK_PROPERTIES } from '../data/mockProperties';
import { ContactFormData, PreferredContact } from '../types/models';

/**
 * Property detail page component.
 *
 * Displays comprehensive information about a single property listing,
 * including photo gallery, property details, description, features,
 * agent card sidebar, and contact form.
 * Responsive layout: main content + sidebar on desktop, stacked on mobile.
 */
const PropertyDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const property = MOCK_PROPERTIES.find((p) => p.id === id);

  const [formData, setFormData] = useState<ContactFormData>({
    name: '',
    email: '',
    phone: '',
    message: property ? `I'm interested in "${property.title}" at ${property.address}. Please send me more information.` : '',
    propertyId: id,
    preferredContact: 'email',
  });
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [galleryIndex, setGalleryIndex] = useState(0);

  if (!property) {
    return (
      <div className="min-h-screen flex flex-col">
        <header className="bg-white shadow-sm border-b border-slate-200">
          <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
            <Link to="/" className="text-2xl font-bold text-blue-600">HomeFind</Link>
            <nav className="hidden md:flex gap-6">
              <Link to="/" className="text-slate-600 hover:text-blue-600 font-medium">Listings</Link>
            </nav>
          </div>
        </header>
        <main className="flex-1 flex flex-col items-center justify-center py-20 px-4">
          <h1 className="text-3xl font-bold text-slate-900 mb-4">Property Not Found</h1>
          <p className="text-slate-500 mb-8">The property you are looking for does not exist.</p>
          <Link to="/" className="text-blue-600 hover:text-blue-700 font-semibold">&larr; Back to Listings</Link>
        </main>
        <footer className="bg-slate-900 text-slate-400 py-8">
          <div className="max-w-7xl mx-auto px-4 text-center text-sm">&copy; {new Date().getFullYear()} HomeFind. All rights reserved.</div>
        </footer>
      </div>
    );
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setFormSubmitted(true);
  };

  const statusLabel: Record<string, string> = { 'for-sale': 'For Sale', pending: 'Pending', sold: 'Sold' };
  const statusColor: Record<string, string> = {
    'for-sale': 'bg-green-100 text-green-800',
    pending: 'bg-yellow-100 text-yellow-800',
    sold: 'bg-red-100 text-red-800',
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-blue-600">HomeFind</Link>
          <nav className="hidden md:flex gap-6">
            <Link to="/" className="text-slate-600 hover:text-blue-600 font-medium">Listings</Link>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        {/* Breadcrumb */}
        <div className="max-w-7xl mx-auto px-4 py-4">
          <Link to="/" className="text-blue-600 hover:text-blue-700 font-medium text-sm">&larr; Back to Listings</Link>
        </div>

        {/* Photo Gallery */}
        <section className="max-w-7xl mx-auto px-4 mb-8">
          <div className="relative">
            <div className="overflow-hidden rounded-xl aspect-[16/9] md:aspect-[2/1]">
              <img
                src={property.images[galleryIndex]}
                alt={`${property.title} — image ${galleryIndex + 1}`}
                className="w-full h-full object-cover transition-opacity duration-300"
              />
            </div>
            {property.images.length > 1 && (
              <>
                <button
                  onClick={() => setGalleryIndex((prev) => (prev === 0 ? property.images.length - 1 : prev - 1))}
                  className="absolute left-3 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white text-slate-800 rounded-full w-10 h-10 flex items-center justify-center shadow-md transition-colors"
                  aria-label="Previous image"
                >
                  &#8249;
                </button>
                <button
                  onClick={() => setGalleryIndex((prev) => (prev === property.images.length - 1 ? 0 : prev + 1))}
                  className="absolute right-3 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white text-slate-800 rounded-full w-10 h-10 flex items-center justify-center shadow-md transition-colors"
                  aria-label="Next image"
                >
                  &#8250;
                </button>
              </>
            )}
            <div className="absolute bottom-3 right-3 bg-black/60 text-white text-xs px-3 py-1 rounded-full">
              {galleryIndex + 1} / {property.images.length}
            </div>
          </div>
          {/* Thumbnails */}
          <div className="flex gap-2 mt-3 overflow-x-auto pb-1">
            {property.images.map((img, i) => (
              <button
                key={i}
                onClick={() => setGalleryIndex(i)}
                className={`flex-shrink-0 w-20 h-14 rounded-lg overflow-hidden border-2 transition-colors ${
                  i === galleryIndex ? 'border-blue-600' : 'border-transparent hover:border-slate-300'
                }`}
              >
                <img src={img} alt={`Thumbnail ${i + 1}`} className="w-full h-full object-cover" />
              </button>
            ))}
          </div>
        </section>

        {/* Content + Sidebar */}
        <section className="max-w-7xl mx-auto px-4 pb-16">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2">
              {/* Status badge */}
              <div className="mb-4">
                <span className={`inline-block text-xs font-semibold px-3 py-1 rounded-full uppercase ${statusColor[property.status] || 'bg-blue-100 text-blue-800'}`}>
                  {statusLabel[property.status] || property.status}
                </span>
              </div>

              {/* Title & Address */}
              <h1 className="text-3xl md:text-4xl font-bold text-slate-900 mb-2">{property.title}</h1>
              <p className="text-slate-500 text-lg mb-2 flex items-center gap-2">
                <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                {property.address}, {property.city}, {property.state} {property.zipCode}
              </p>
              <p className="text-3xl font-bold text-blue-600 mb-8">${property.price.toLocaleString()}</p>

              {/* Stats with icons */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
                <div className="bg-white rounded-lg p-4 shadow-sm text-center">
                  <svg className="w-6 h-6 mx-auto mb-1 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0h4" /></svg>
                  <p className="text-2xl font-bold text-slate-900">{property.bedrooms}</p>
                  <p className="text-sm text-slate-500">Bedrooms</p>
                </div>
                <div className="bg-white rounded-lg p-4 shadow-sm text-center">
                  <svg className="w-6 h-6 mx-auto mb-1 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4" /></svg>
                  <p className="text-2xl font-bold text-slate-900">{property.bathrooms}</p>
                  <p className="text-sm text-slate-500">Bathrooms</p>
                </div>
                <div className="bg-white rounded-lg p-4 shadow-sm text-center">
                  <svg className="w-6 h-6 mx-auto mb-1 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" /></svg>
                  <p className="text-2xl font-bold text-slate-900">{property.squareFeet.toLocaleString()}</p>
                  <p className="text-sm text-slate-500">Sq Ft</p>
                </div>
                <div className="bg-white rounded-lg p-4 shadow-sm text-center">
                  <svg className="w-6 h-6 mx-auto mb-1 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                  <p className="text-2xl font-bold text-slate-900">{property.yearBuilt}</p>
                  <p className="text-sm text-slate-500">Year Built</p>
                </div>
              </div>

              {/* Description */}
              <div className="mb-8">
                <h2 className="text-xl font-bold text-slate-900 mb-3">About This Property</h2>
                <p className="text-slate-600 leading-relaxed">{property.description}</p>
              </div>

              {/* Property Details */}
              <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
                <h2 className="text-xl font-bold text-slate-900 mb-4">Property Details</h2>
                <div className="grid grid-cols-2 gap-y-3 gap-x-8 text-sm">
                  <div className="flex justify-between border-b border-slate-100 pb-2">
                    <span className="text-slate-500">Property Type</span>
                    <span className="text-slate-900 font-medium capitalize">{property.propertyType}</span>
                  </div>
                  <div className="flex justify-between border-b border-slate-100 pb-2">
                    <span className="text-slate-500">Status</span>
                    <span className="text-slate-900 font-medium capitalize">{statusLabel[property.status]}</span>
                  </div>
                  <div className="flex justify-between border-b border-slate-100 pb-2">
                    <span className="text-slate-500">Bedrooms</span>
                    <span className="text-slate-900 font-medium">{property.bedrooms}</span>
                  </div>
                  <div className="flex justify-between border-b border-slate-100 pb-2">
                    <span className="text-slate-500">Bathrooms</span>
                    <span className="text-slate-900 font-medium">{property.bathrooms}</span>
                  </div>
                  <div className="flex justify-between border-b border-slate-100 pb-2">
                    <span className="text-slate-500">Square Feet</span>
                    <span className="text-slate-900 font-medium">{property.squareFeet.toLocaleString()}</span>
                  </div>
                  {property.lotSize && (
                    <div className="flex justify-between border-b border-slate-100 pb-2">
                      <span className="text-slate-500">Lot Size</span>
                      <span className="text-slate-900 font-medium">{property.lotSize}</span>
                    </div>
                  )}
                  <div className="flex justify-between border-b border-slate-100 pb-2">
                    <span className="text-slate-500">Year Built</span>
                    <span className="text-slate-900 font-medium">{property.yearBuilt}</span>
                  </div>
                  <div className="flex justify-between border-b border-slate-100 pb-2">
                    <span className="text-slate-500">Listed</span>
                    <span className="text-slate-900 font-medium">{new Date(property.listingDate).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>

              {/* Features */}
              <div className="mb-8">
                <h2 className="text-xl font-bold text-slate-900 mb-4">Features &amp; Amenities</h2>
                <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {property.features.map((feature, i) => (
                    <li key={i} className="flex items-center gap-2 text-slate-600">
                      <svg className="w-5 h-5 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1 space-y-6">
              {/* Agent Card */}
              <div className="bg-white rounded-xl shadow-sm p-6 sticky top-24">
                <h3 className="text-lg font-bold text-slate-900 mb-4">Listing Agent</h3>
                <div className="flex items-center gap-4 mb-4">
                  <img
                    src={property.agent.photo}
                    alt={property.agent.name}
                    className="w-16 h-16 rounded-full object-cover"
                  />
                  <div>
                    <p className="font-semibold text-slate-900">{property.agent.name}</p>
                    <p className="text-sm text-slate-500">{property.agent.title}</p>
                    <div className="flex items-center gap-1 mt-1">
                      <svg className="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" /></svg>
                      <span className="text-sm text-slate-600">{property.agent.rating}</span>
                      <span className="text-xs text-slate-400">• {property.agent.propertiesCount} listings</span>
                    </div>
                  </div>
                </div>
                <p className="text-sm text-slate-600 mb-4 line-clamp-3">{property.agent.bio}</p>
                <div className="space-y-2 mb-4">
                  <a href={`tel:${property.agent.phone}`} className="flex items-center gap-2 text-sm text-slate-600 hover:text-blue-600">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
                    {property.agent.phone}
                  </a>
                  <a href={`mailto:${property.agent.email}`} className="flex items-center gap-2 text-sm text-slate-600 hover:text-blue-600">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
                    {property.agent.email}
                  </a>
                </div>
                <div className="flex flex-wrap gap-1">
                  {property.agent.specialties.map((spec, i) => (
                    <span key={i} className="text-xs bg-slate-100 text-slate-600 px-2 py-1 rounded-full">{spec}</span>
                  ))}
                </div>
              </div>

              {/* Contact Form */}
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h3 className="text-lg font-bold text-slate-900 mb-4">Schedule a Tour</h3>
                {formSubmitted ? (
                  <div className="text-center py-6">
                    <svg className="w-12 h-12 text-green-500 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    <p className="text-lg font-semibold text-slate-900">Message Sent!</p>
                    <p className="text-sm text-slate-500 mt-1">We'll get back to you shortly.</p>
                    <button onClick={() => setFormSubmitted(false)} className="mt-4 text-blue-600 hover:text-blue-700 text-sm font-medium">Send another message</button>
                  </div>
                ) : (
                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                      <label htmlFor="name" className="block text-sm font-medium text-slate-700 mb-1">Full Name</label>
                      <input id="name" name="name" type="text" required value={formData.name} onChange={handleInputChange} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="John Doe" />
                    </div>
                    <div>
                      <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-1">Email</label>
                      <input id="email" name="email" type="email" required value={formData.email} onChange={handleInputChange} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="john@example.com" />
                    </div>
                    <div>
                      <label htmlFor="phone" className="block text-sm font-medium text-slate-700 mb-1">Phone</label>
                      <input id="phone" name="phone" type="tel" value={formData.phone} onChange={handleInputChange} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="(555) 123-4567" />
                    </div>
                    <div>
                      <label htmlFor="preferredContact" className="block text-sm font-medium text-slate-700 mb-1">Preferred Contact</label>
                      <select id="preferredContact" name="preferredContact" value={formData.preferredContact} onChange={handleInputChange} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        <option value="email">Email</option>
                        <option value="phone">Phone</option>
                        <option value="either">Either</option>
                      </select>
                    </div>
                    <div>
                      <label htmlFor="message" className="block text-sm font-medium text-slate-700 mb-1">Message</label>
                      <textarea id="message" name="message" rows={4} required value={formData.message} onChange={handleInputChange} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" />
                    </div>
                    <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition-colors">
                      Send Message
                    </button>
                  </form>
                )}
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400">
        <div className="max-w-7xl mx-auto px-4 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            <div>
              <h4 className="text-white text-lg font-bold mb-3">HomeFind</h4>
              <p className="text-sm">Helping you discover your perfect home since 2020. We connect buyers with the finest properties across Austin, Texas.</p>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-3">Quick Links</h4>
              <ul className="space-y-2 text-sm">
                <li><Link to="/" className="hover:text-white transition-colors">Listings</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-3">Contact Us</h4>
              <ul className="space-y-2 text-sm">
                <li>123 Main Street, Austin, TX 78701</li>
                <li>(555) 000-1234</li>
                <li>info@homefind.com</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-slate-800 pt-6 text-center text-sm">
            &copy; {new Date().getFullYear()} HomeFind. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default PropertyDetailPage;
