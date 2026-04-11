import React, { useState } from 'react';

/** Shape of the contact form data. */
interface ContactFormData {
  name: string;
  email: string;
  message: string;
}

/** Shape of form validation errors. */
interface FormErrors {
  name?: string;
  email?: string;
  message?: string;
}

/**
 * ContactInfo component.
 * Displays contact information (phone, email, address) and a contact form
 * with client-side validation for required fields.
 */
export const ContactInfo: React.FC = () => {
  const [formData, setFormData] = useState<ContactFormData>({
    name: '',
    email: '',
    message: '',
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [submitted, setSubmitted] = useState<boolean>(false);

  /** Validate form fields and return errors object. */
  const validate = (data: ContactFormData): FormErrors => {
    const newErrors: FormErrors = {};

    if (!data.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!data.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!data.message.trim()) {
      newErrors.message = 'Message is required';
    }

    return newErrors;
  };

  /** Handle input changes. */
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ): void => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    // Clear the error for this field when user starts typing
    if (errors[name as keyof FormErrors]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  /** Handle form submission. */
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    const validationErrors = validate(formData);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setSubmitted(true);
    setFormData({ name: '', email: '', message: '' });
    setErrors({});
  };

  return (
    <section className="contact-section" data-testid="contact-info">
      <h2 className="section-heading">Contact Us</h2>

      <div className="contact-content">
        <div className="contact-details">
          <div className="contact-item">
            <strong>Phone:</strong>
            <a href="tel:+15551234567" data-testid="contact-phone">
              (555) 123-4567
            </a>
          </div>
          <div className="contact-item">
            <strong>Email:</strong>
            <a href="mailto:info@madhurirealestate.com" data-testid="contact-email">
              info@madhurirealestate.com
            </a>
          </div>
          <div className="contact-item">
            <strong>Address:</strong>
            <span data-testid="contact-address">
              100 Main Street, Suite 200, Springfield, IL 62701
            </span>
          </div>
        </div>

        <form
          className="contact-form"
          onSubmit={handleSubmit}
          data-testid="contact-form"
          noValidate
        >
          {submitted && (
            <div className="form-success" data-testid="form-success">
              Thank you for your message! We will get back to you soon.
            </div>
          )}

          <div className="form-group">
            <label htmlFor="contact-name">Name *</label>
            <input
              id="contact-name"
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              aria-describedby={errors.name ? 'name-error' : undefined}
              aria-invalid={!!errors.name}
            />
            {errors.name && (
              <span id="name-error" className="form-error" data-testid="error-name">
                {errors.name}
              </span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="contact-email">Email *</label>
            <input
              id="contact-email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              aria-describedby={errors.email ? 'email-error' : undefined}
              aria-invalid={!!errors.email}
            />
            {errors.email && (
              <span id="email-error" className="form-error" data-testid="error-email">
                {errors.email}
              </span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="contact-message">Message *</label>
            <textarea
              id="contact-message"
              name="message"
              rows={5}
              value={formData.message}
              onChange={handleChange}
              aria-describedby={errors.message ? 'message-error' : undefined}
              aria-invalid={!!errors.message}
            />
            {errors.message && (
              <span
                id="message-error"
                className="form-error"
                data-testid="error-message"
              >
                {errors.message}
              </span>
            )}
          </div>

          <button type="submit" className="btn-submit">
            Send Message
          </button>
        </form>
      </div>
    </section>
  );
};
