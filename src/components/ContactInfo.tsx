import React, { useState, FormEvent, ChangeEvent } from 'react';

/** Shape of the contact form fields. */
interface FormData {
  name: string;
  email: string;
  message: string;
}

/** Shape of per-field validation errors. */
interface FormErrors {
  name?: string;
  email?: string;
  message?: string;
}

/**
 * Validates form data and returns an object of field-level error messages.
 * Returns an empty object when all fields are valid.
 */
function validateForm(data: FormData): FormErrors {
  const errors: FormErrors = {};

  if (!data.name.trim()) {
    errors.name = 'Name is required';
  }

  if (!data.email.trim()) {
    errors.email = 'Email is required';
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email.trim())) {
    errors.email = 'Please enter a valid email address';
  }

  if (!data.message.trim()) {
    errors.message = 'Message is required';
  }

  return errors;
}

/**
 * ContactInfo component displays contact details (phone, email, address)
 * alongside a validated contact form. Form validation is performed on
 * submission and inline errors are displayed for each invalid field.
 */
const ContactInfo: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    message: '',
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [submitted, setSubmitted] = useState<boolean>(false);

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>): void => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear field error on change
    if (errors[name as keyof FormErrors]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    const validationErrors = validateForm(formData);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      setSubmitted(false);
      return;
    }

    // In a real application, this would send the data to a server.
    setErrors({});
    setSubmitted(true);
    setFormData({ name: '', email: '', message: '' });
  };

  return (
    <section className="contact-section" data-testid="contact-section" aria-label="Contact Information">
      <h2>Get In Touch</h2>
      <div className="contact-layout">
        {/* Contact Details */}
        <div className="contact-details" data-testid="contact-details">
          <div className="contact-item">
            <span className="contact-label">Phone:</span>
            <a href="tel:+15551234567" aria-label="Call us at (555) 123-4567">(555) 123-4567</a>
          </div>
          <div className="contact-item">
            <span className="contact-label">Email:</span>
            <a href="mailto:info@madhurirealestate.com" aria-label="Email us at info@madhurirealestate.com">
              info@madhurirealestate.com
            </a>
          </div>
          <div className="contact-item">
            <span className="contact-label">Address:</span>
            <span>100 Main Street, Suite 200, Springfield, IL 62701</span>
          </div>
        </div>

        {/* Contact Form */}
        <form className="contact-form" data-testid="contact-form" onSubmit={handleSubmit} noValidate>
          {submitted && (
            <div className="form-success" data-testid="form-success" role="status">
              Thank you! Your message has been sent.
            </div>
          )}

          <div className="form-group">
            <label htmlFor="contact-name">Name</label>
            <input
              id="contact-name"
              name="name"
              type="text"
              value={formData.name}
              onChange={handleChange}
              aria-required="true"
              aria-invalid={!!errors.name}
              placeholder="Your name"
            />
            {errors.name && (
              <span className="field-error" data-testid="error-name" role="alert">
                {errors.name}
              </span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="contact-email">Email</label>
            <input
              id="contact-email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              aria-required="true"
              aria-invalid={!!errors.email}
              placeholder="you@example.com"
            />
            {errors.email && (
              <span className="field-error" data-testid="error-email" role="alert">
                {errors.email}
              </span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="contact-message">Message</label>
            <textarea
              id="contact-message"
              name="message"
              value={formData.message}
              onChange={handleChange}
              aria-required="true"
              aria-invalid={!!errors.message}
              placeholder="How can we help you?"
            />
            {errors.message && (
              <span className="field-error" data-testid="error-message" role="alert">
                {errors.message}
              </span>
            )}
          </div>

          <button type="submit">Send Message</button>
        </form>
      </div>
    </section>
  );
};

export default ContactInfo;
