import React, { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import type { ContactFormData, PreferredContact } from "../types/models";

/**
 * Contact page component.
 *
 * Renders a contact form that collects user inquiry details.
 * Optionally pre-fills a propertyId when linked from a property detail page.
 */
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

  const [submitted, setSubmitted] = useState<boolean>(false);

  /**
   * Handle input field changes and update form state.
   */
  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
  ): void => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  /**
   * Handle form submission.
   */
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    // In a real app this would POST to an API
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <main className="flex-1 flex flex-col items-center justify-center py-20 px-4">
        <div className="bg-white rounded-xl shadow-sm p-10 text-center max-w-md">
          <h1 className="text-2xl font-bold text-slate-900 mb-4">
            Thank You!
          </h1>
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
      </main>
    );
  }

  return (
    <main className="flex-1">
      {/* Navigation */}
      <div className="max-w-3xl mx-auto px-4 py-4">
        <Link
          to="/"
          className="text-blue-600 hover:text-blue-700 font-medium text-sm"
        >
          &larr; Back to Listings
        </Link>
      </div>

      <section className="max-w-3xl mx-auto px-4 pb-16">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Contact Us</h1>
        <p className="text-slate-500 mb-8">
          Have a question or want to schedule a viewing? Fill out the form below
          and we&apos;ll be in touch.
        </p>

        <form
          onSubmit={handleSubmit}
          className="bg-white rounded-xl shadow-sm p-6 md:p-8 space-y-6"
        >
          {/* Name */}
          <div>
            <label
              htmlFor="name"
              className="block text-sm font-medium text-slate-700 mb-1"
            >
              Full Name
            </label>
            <input
              type="text"
              id="name"
              name="name"
              required
              value={formData.name}
              onChange={handleChange}
              className="w-full border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="John Doe"
            />
          </div>

          {/* Email */}
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-slate-700 mb-1"
            >
              Email Address
            </label>
            <input
              type="email"
              id="email"
              name="email"
              required
              value={formData.email}
              onChange={handleChange}
              className="w-full border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="john@example.com"
            />
          </div>

          {/* Phone */}
          <div>
            <label
              htmlFor="phone"
              className="block text-sm font-medium text-slate-700 mb-1"
            >
              Phone Number
            </label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              className="w-full border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="(555) 123-4567"
            />
          </div>

          {/* Preferred Contact */}
          <div>
            <label
              htmlFor="preferredContact"
              className="block text-sm font-medium text-slate-700 mb-1"
            >
              Preferred Contact Method
            </label>
            <select
              id="preferredContact"
              name="preferredContact"
              value={formData.preferredContact}
              onChange={handleChange}
              className="w-full border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="email">Email</option>
              <option value="phone">Phone</option>
              <option value="either">Either</option>
            </select>
          </div>

          {/* Message */}
          <div>
            <label
              htmlFor="message"
              className="block text-sm font-medium text-slate-700 mb-1"
            >
              Message
            </label>
            <textarea
              id="message"
              name="message"
              required
              rows={5}
              value={formData.message}
              onChange={handleChange}
              className="w-full border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-vertical"
              placeholder="I'm interested in scheduling a viewing..."
            />
          </div>

          {propertyId && (
            <input type="hidden" name="propertyId" value={propertyId} />
          )}

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
          >
            Send Message
          </button>
        </form>
      </section>
    </main>
  );
};

export default ContactPage;
