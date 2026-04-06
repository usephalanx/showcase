import React, { useState, useCallback } from 'react';
import Input from './Input';
import Button from './Button';

export interface ContactFormProps {
  /** Optional property title to pre-fill the property interest field */
  propertyTitle?: string;
  /** Optional agent name to display in the form header */
  agentName?: string;
  /** List of property options for the interest dropdown */
  propertyOptions?: string[];
  /** Callback fired with form data on valid submission */
  onSubmit?: (data: ContactFormData) => void;
}

export interface ContactFormData {
  name: string;
  email: string;
  phone: string;
  message: string;
  propertyInterest: string;
  preferredContact: 'email' | 'phone';
}

interface FormErrors {
  name?: string;
  email?: string;
  phone?: string;
  message?: string;
  propertyInterest?: string;
}

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const INITIAL_DATA: ContactFormData = {
  name: '',
  email: '',
  phone: '',
  message: '',
  propertyInterest: '',
  preferredContact: 'email',
};

export default function ContactForm({
  propertyTitle,
  agentName,
  propertyOptions = [],
  onSubmit,
}: ContactFormProps) {
  const [formData, setFormData] = useState<ContactFormData>({
    ...INITIAL_DATA,
    propertyInterest: propertyTitle ?? '',
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [submitted, setSubmitted] = useState(false);

  const validate = useCallback((): FormErrors => {
    const errs: FormErrors = {};
    if (!formData.name.trim()) errs.name = 'Name is required';
    if (!formData.email.trim()) {
      errs.email = 'Email is required';
    } else if (!EMAIL_REGEX.test(formData.email)) {
      errs.email = 'Please enter a valid email address';
    }
    if (!formData.phone.trim()) errs.phone = 'Phone number is required';
    if (!formData.message.trim()) errs.message = 'Message is required';
    if (!formData.propertyInterest.trim())
      errs.propertyInterest = 'Please select a property of interest';
    return errs;
  }, [formData]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name as keyof FormErrors]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }
    setErrors({});
    onSubmit?.(formData);
    setSubmitted(true);
    setFormData({ ...INITIAL_DATA, propertyInterest: propertyTitle ?? '' });
  };

  const dismissSuccess = () => setSubmitted(false);

  const dropdownOptions = propertyTitle
    ? [propertyTitle, ...propertyOptions.filter((o) => o !== propertyTitle)]
    : propertyOptions;

  return (
    <form onSubmit={handleSubmit} className="space-y-5 max-w-lg" noValidate>
      {agentName && (
        <p className="text-sm text-gray-600" data-testid="agent-label">
          Contact <span className="font-semibold">{agentName}</span>
        </p>
      )}

      {submitted && (
        <div
          role="status"
          data-testid="success-message"
          className="flex items-center justify-between rounded-md bg-green-50 border border-green-300 px-4 py-3 text-green-800 text-sm"
        >
          <span>Your message has been sent successfully!</span>
          <button
            type="button"
            onClick={dismissSuccess}
            className="ml-4 font-bold text-green-700 hover:text-green-900"
            aria-label="Dismiss success message"
          >
            ×
          </button>
        </div>
      )}

      <div>
        <Input
          name="name"
          placeholder="Full Name"
          value={formData.name}
          onChange={handleChange}
          aria-required="true"
          aria-invalid={!!errors.name}
        />
        {errors.name && <p className="mt-1 text-sm text-red-600" role="alert">{errors.name}</p>}
      </div>

      <div>
        <Input
          name="email"
          type="email"
          placeholder="Email Address"
          value={formData.email}
          onChange={handleChange}
          aria-required="true"
          aria-invalid={!!errors.email}
        />
        {errors.email && <p className="mt-1 text-sm text-red-600" role="alert">{errors.email}</p>}
      </div>

      <div>
        <Input
          name="phone"
          type="tel"
          placeholder="Phone Number"
          value={formData.phone}
          onChange={handleChange}
          aria-required="true"
          aria-invalid={!!errors.phone}
        />
        {errors.phone && <p className="mt-1 text-sm text-red-600" role="alert">{errors.phone}</p>}
      </div>

      <div>
        <select
          name="propertyInterest"
          value={formData.propertyInterest}
          onChange={handleChange}
          aria-required="true"
          aria-invalid={!!errors.propertyInterest}
          className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        >
          <option value="">Select a property of interest</option>
          {dropdownOptions.map((opt) => (
            <option key={opt} value={opt}>
              {opt}
            </option>
          ))}
        </select>
        {errors.propertyInterest && (
          <p className="mt-1 text-sm text-red-600" role="alert">{errors.propertyInterest}</p>
        )}
      </div>

      <fieldset>
        <legend className="text-sm font-medium text-gray-700 mb-2">Preferred Contact Method</legend>
        <div className="flex gap-6">
          <label className="flex items-center gap-2 text-sm cursor-pointer">
            <input
              type="radio"
              name="preferredContact"
              value="email"
              checked={formData.preferredContact === 'email'}
              onChange={handleChange}
              className="accent-blue-600"
            />
            Email
          </label>
          <label className="flex items-center gap-2 text-sm cursor-pointer">
            <input
              type="radio"
              name="preferredContact"
              value="phone"
              checked={formData.preferredContact === 'phone'}
              onChange={handleChange}
              className="accent-blue-600"
            />
            Phone
          </label>
        </div>
      </fieldset>

      <div>
        <textarea
          name="message"
          placeholder="Your message..."
          value={formData.message}
          onChange={handleChange}
          rows={4}
          aria-required="true"
          aria-invalid={!!errors.message}
          className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 resize-vertical"
        />
        {errors.message && <p className="mt-1 text-sm text-red-600" role="alert">{errors.message}</p>}
      </div>

      <Button type="submit">Send Message</Button>
    </form>
  );
}
