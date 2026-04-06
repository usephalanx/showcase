import React, { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import type { ContactFormData, PreferredContact } from "../types/models";

const HERO_IMAGE =
  "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=1600&h=400&fit=crop";

const AGENT = {
  name: "Sarah Mitchell",
  title: "Senior Real Estate Agent",
  phone: "(555) 234-5678",
  email: "sarah@premierrealty.com",
  photo:
    "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop",
  bio: "With over 12 years of experience in residential real estate, Sarah is dedicated to helping clients find their perfect home. She specializes in luxury properties and first-time homebuyers alike.",
  specialties: ["Luxury Homes", "First-Time Buyers", "Investment Properties"],
  rating: 4.9,
};

const OFFICE = {
  address: "742 Evergreen Terrace, Suite 200",
  city: "Springfield, IL 62704",
  phone: "(555) 123-4567",
  email: "info@premierrealty.com",
  hours: [
    { days: "Monday – Friday", time: "9:00 AM – 6:00 PM" },
    { days: "Saturday", time: "10:00 AM – 4:00 PM" },
    { days: "Sunday", time: "Closed" },
  ],
};

const ContactPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const propertyId = searchParams.get("propertyId") ?? undefined;

  const [formData, setFormData] = useState<ContactFormData>({
    name: "",
    email: "",
    phone: "",
    message: "",
    propertyId,
    preferredContact: "email",
  });

  const [submitted, setSubmitted] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ): void => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
          <Link to="/" className="text-xl font-bold text-blue-600 tracking-tight">
            Premier Realty
          </Link>
          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600">
            <Link to="/" className="hover:text-blue-600 transition-colors">Home</Link>
            <Link to="/properties" className="hover:text-blue-600 transition-colors">Properties</Link>
            <Link to="/neighborhoods" className="hover:text-blue-600 transition-colors">Neighborhoods</Link>
            <Link to="/contact" className="text-blue-600 font-semibold">Contact</Link>
          </nav>
        </div>
      </header>

      {/* Hero Banner */}
      <section
        className="relative h-48 sm:h-56 md:h-64 bg-cover bg-center"
        style={{ backgroundImage: `url(${HERO_IMAGE})` }}
      >
        <div className="absolute inset-0 bg-slate-900/60" />
        <div className="relative z-10 flex flex-col items-center justify-center h-full text-center px-4">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-2">
            Get In Touch
          </h1>
          <p className="text-slate-200 text-sm sm:text-base max-w-lg">
            We&apos;d love to hear from you. Reach out with any questions about properties, buying, or selling.
          </p>
        </div>
      </section>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12">
        {submitted ? (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="bg-white rounded-xl shadow-sm p-10 text-center max-w-md">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-slate-900 mb-4">Thank You!</h2>
              <p className="text-slate-600 mb-8">
                Your message has been sent. We&apos;ll get back to you shortly.
              </p>
              <Link
                to="/"
                className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors"
              >
                Back to Home
              </Link>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
            {/* Left Column — Contact Form (2/3 width on desktop) */}
            <div className="lg:col-span-2 space-y-8">
              <form
                onSubmit={handleSubmit}
                className="bg-white rounded-xl shadow-sm p-6 md:p-8 space-y-6"
              >
                <h2 className="text-xl font-bold text-slate-900">Send Us a Message</h2>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-slate-700 mb-1">Full Name</label>
                    <input type="text" id="name" name="name" required value={formData.name} onChange={handleChange}
                      className="w-full border border-slate-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="John Doe" />
                  </div>
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-1">Email Address</label>
                    <input type="email" id="email" name="email" required value={formData.email} onChange={handleChange}
                      className="w-full border border-slate-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="john@example.com" />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="phone" className="block text-sm font-medium text-slate-700 mb-1">Phone Number</label>
                    <input type="tel" id="phone" name="phone" value={formData.phone} onChange={handleChange}
                      className="w-full border border-slate-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="(555) 000-0000" />
                  </div>
                  <div>
                    <label htmlFor="preferredContact" className="block text-sm font-medium text-slate-700 mb-1">Preferred Contact</label>
                    <select id="preferredContact" name="preferredContact" value={formData.preferredContact} onChange={handleChange}
                      className="w-full border border-slate-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white">
                      <option value="email">Email</option>
                      <option value="phone">Phone</option>
                      <option value="either">Either</option>
                    </select>
                  </div>
                </div>

                {propertyId && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg px-4 py-3 text-sm text-blue-700">
                    Inquiry regarding property <span className="font-semibold">#{propertyId}</span>
                  </div>
                )}

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-slate-700 mb-1">Message</label>
                  <textarea id="message" name="message" required rows={5} value={formData.message} onChange={handleChange}
                    className="w-full border border-slate-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-vertical"
                    placeholder="Tell us how we can help…" />
                </div>

                <button type="submit"
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors text-base">
                  Send Message
                </button>
              </form>

              {/* Embedded Map Placeholder */}
              <div className="bg-slate-200 rounded-xl h-64 flex items-center justify-center">
                <div className="text-center">
                  <svg className="w-10 h-10 text-slate-400 mx-auto mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                  </svg>
                  <p className="text-slate-500 font-medium text-sm">742 Evergreen Terrace, Springfield, IL 62704</p>
                  <p className="text-slate-400 text-xs mt-1">Interactive map would be displayed here</p>
                </div>
              </div>
            </div>

            {/* Right Column — Office Info + Agent */}
            <div className="space-y-8">
              {/* Office Location Card */}
              <div className="bg-white rounded-xl shadow-sm p-6 space-y-5">
                <h3 className="text-lg font-bold text-slate-900">Our Office</h3>

                <div className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-blue-600 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                  </svg>
                  <div className="text-sm text-slate-600 leading-relaxed">
                    <p>{OFFICE.address}</p>
                    <p>{OFFICE.city}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <svg className="w-5 h-5 text-blue-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z" />
                  </svg>
                  <a href={`tel:${OFFICE.phone}`} className="text-sm text-slate-600 hover:text-blue-600 transition-colors">{OFFICE.phone}</a>
                </div>

                <div className="flex items-center gap-3">
                  <svg className="w-5 h-5 text-blue-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                  </svg>
                  <a href={`mailto:${OFFICE.email}`} className="text-sm text-slate-600 hover:text-blue-600 transition-colors">{OFFICE.email}</a>
                </div>

                <div className="border-t border-slate-100 pt-4">
                  <h4 className="text-sm font-semibold text-slate-800 mb-2">Office Hours</h4>
                  <ul className="space-y-1">
                    {OFFICE.hours.map((h) => (
                      <li key={h.days} className="flex justify-between text-sm">
                        <span className="text-slate-500">{h.days}</span>
                        <span className="text-slate-700 font-medium">{h.time}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Agent Profile Section */}
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h3 className="text-lg font-bold text-slate-900 mb-4">Your Agent</h3>
                <div className="flex items-center gap-4 mb-4">
                  <img
                    src={AGENT.photo}
                    alt={AGENT.name}
                    className="w-16 h-16 rounded-full object-cover"
                    loading="lazy"
                  />
                  <div>
                    <p className="font-semibold text-slate-900">{AGENT.name}</p>
                    <p className="text-sm text-slate-500">{AGENT.title}</p>
                    <div className="flex items-center gap-1 mt-1">
                      <svg className="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                      <span className="text-sm text-slate-600 font-medium">{AGENT.rating}</span>
                    </div>
                  </div>
                </div>
                <p className="text-sm text-slate-600 leading-relaxed mb-4">{AGENT.bio}</p>
                <div className="flex flex-wrap gap-2 mb-4">
                  {AGENT.specialties.map((s) => (
                    <span key={s} className="bg-blue-50 text-blue-700 text-xs font-medium px-2.5 py-1 rounded-full">{s}</span>
                  ))}
                </div>
                <div className="space-y-2 text-sm">
                  <a href={`tel:${AGENT.phone}`} className="flex items-center gap-2 text-slate-600 hover:text-blue-600 transition-colors">
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z" />
                    </svg>
                    {AGENT.phone}
                  </a>
                  <a href={`mailto:${AGENT.email}`} className="flex items-center gap-2 text-slate-600 hover:text-blue-600 transition-colors">
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                    </svg>
                    {AGENT.email}
                  </a>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            <div>
              <h4 className="text-white font-bold text-lg mb-3">Premier Realty</h4>
              <p className="text-sm leading-relaxed">Helping you find the perfect place to call home since 2010.</p>
            </div>
            <div>
              <h5 className="text-white font-semibold text-sm mb-3">Quick Links</h5>
              <ul className="space-y-2 text-sm">
                <li><Link to="/" className="hover:text-white transition-colors">Home</Link></li>
                <li><Link to="/properties" className="hover:text-white transition-colors">Properties</Link></li>
                <li><Link to="/neighborhoods" className="hover:text-white transition-colors">Neighborhoods</Link></li>
                <li><Link to="/contact" className="hover:text-white transition-colors">Contact</Link></li>
              </ul>
            </div>
            <div>
              <h5 className="text-white font-semibold text-sm mb-3">Contact</h5>
              <ul className="space-y-2 text-sm">
                <li>{OFFICE.address}</li>
                <li>{OFFICE.city}</li>
                <li>{OFFICE.phone}</li>
                <li>{OFFICE.email}</li>
              </ul>
            </div>
            <div>
              <h5 className="text-white font-semibold text-sm mb-3">Office Hours</h5>
              <ul className="space-y-1 text-sm">
                {OFFICE.hours.map((h) => (
                  <li key={h.days}>{h.days}: {h.time}</li>
                ))}
              </ul>
            </div>
          </div>
          <div className="border-t border-slate-800 mt-10 pt-6 text-center text-sm">
            <p>&copy; {new Date().getFullYear()} Premier Realty. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default ContactPage;
