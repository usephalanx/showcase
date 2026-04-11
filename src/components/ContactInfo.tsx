import React, { useState } from 'react';

/** Shape of the contact form data. */
interface FormData {
  name: string;
  email: string;
  phone: string;
  message: string;
}

/** Shape of form validation errors. */
interface FormErrors {
  name?: string;
  email?: string;
  message?: string;
}

/**
 * ContactInfo component displays phone, email, and address information
 * alongside a simple contact form with client-side validation.
 *
 * Validation rules:
 * - Name is required
 * - Email is required and must be a valid email format
 * - Message is required
 */
const ContactInfo: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    phone: '',
    message: '',
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [submitted, setSubmitted] = useState<boolean>(false);

  /**
   * Validate all form fields and return an errors object.
   * Returns an empty object if validation passes.
   */
  const validate = (): FormErrors => {
    const newErrors: FormErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email.trim())) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!formData.message.trim()) {
      newErrors.message = 'Message is required';
    }

    return newErrors;
  };

  /** Handle input changes and clear field-level errors on edit. */
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ): void => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    // Clear error for this field when user starts typing
    if (errors[name as keyof FormErrors]) {
      setErrors((prev) => {
        const updated = { ...prev };
        delete updated[name as keyof FormErrors];
        return updated;
      });
    }
  };

  /** Handle form submission with validation. */
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    setSubmitted(false);

    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    setSubmitted(true);
    setFormData({ name: '', email: '', phone: '', message: '' });
  };

  return (
    <section className="section contact-section" data-testid="contact-section">
      <h2>Contact Us</h2>
      <div className="contact-layout">
        {/* Contact Details */}
        <div className="contact-details">
          <div className="contact-item">
            <span className="contact-icon" aria-hidden="true">
              \u260E
            </span>
            <div>
              <p className="contact-label">Phone</p>
              <p className="contact-value" data-testid="contact-phone">
                (555) 123-4567
              </p>
            </div>
          </div>

          <div className="contact-item">
            <span className="contact-icon" aria-hidden="true">
              \u2709
            </span>
            <div>
              <p className="contact-label">Email</p>
              <p className="contact-value" data-testid="contact-email">
                madhuri@madhurirealestate.com
              </p>
            </div>
          </div>

          <div className="contact-item">
            <span className="contact-icon" aria-hidden="true">
              \u2302
            </span>
            <div>
              <p className="contact-label">Address</p>
              <p className="contact-value" data-testid="contact-address">
                100 Main Street, Suite 200
                <br />
                Springfield, IL 62701
              </p>
            </div>
          </div>
        </div>

        {/* Contact Form */}
        <form
          className="contact-form"
          onSubmit={handleSubmit}
          noValidate
          data-testid="contact-form"
        >
          <div className="form-group">
            <label htmlFor="contact-name">Name *</label>
            <input
              type="text"
              id="contact-name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className={errors.name ? 'error' : ''}
              placeholder="Your full name"
              aria-describedby={errors.name ? 'name-error' : undefined}
            />
            {errors.name && (
              <p className="error-message" id="name-error" data-testid="name-error">
                {errors.name}
              </p>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="contact-email">Email *</label>
            <input
              type="email"
              id="contact-email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={errors.email ? 'error' : ''}
              placeholder="your@email.com"
              aria-describedby={errors.email ? 'email-error' : undefined}
            />
            {errors.email && (
              <p className="error-message" id="email-error" data-testid="email-error">
                {errors.email}
              </p>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="contact-phone">Phone</label>
            <input
              type="tel"
              id="contact-phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="(555) 000-0000"
            />
          </div>

          <div className="form-group">
            <label htmlFor="contact-message">Message *</label>
            <textarea
              id="contact-message"
              name="message"
              value={formData.message}
              onChange={handleChange}
              className={errors.message ? 'error' : ''}
              placeholder="How can we help you?"
              aria-describedby={errors.message ? 'message-error' : undefined}
            />
            {errors.message && (
              <p
                className="error-message"
                id="message-error"
                data-testid="message-error"
              >
                {errors.message}
              </p>
            )}
          </div>

          <button type="submit" className="submit-button">
            Send Message
          </button>

          {submitted && (
            <p className="form-success" data-testid="form-success">
              Thank you! Your message has been sent successfully.
            </p>
          )}
        </form>
      </div>
    </section>
  );
};

export default ContactInfo;
