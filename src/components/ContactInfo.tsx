import React, { useState } from 'react';

/**
 * Shape of the contact form data.
 */
interface ContactFormData {
  name: string;
  email: string;
  message: string;
}

/**
 * Shape of validation errors.
 */
interface FormErrors {
  name?: string;
  email?: string;
  message?: string;
}

/**
 * ContactInfo component provides clear contact information
 * (phone, email, address) and a contact form with validation.
 */
const ContactInfo: React.FC = () => {
  const [formData, setFormData] = useState<ContactFormData>({
    name: '',
    email: '',
    message: '',
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [submitted, setSubmitted] = useState<boolean>(false);

  /**
   * Validate the contact form fields.
   * Returns an object with error messages for invalid fields.
   */
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

  /**
   * Handle input changes and clear the field error on change.
   */
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ): void => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name as keyof FormErrors]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  /**
   * Handle form submission with validation.
   */
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    const validationErrors = validate(formData);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      setSubmitted(false);
      return;
    }

    setErrors({});
    setSubmitted(true);
    setFormData({ name: '', email: '', message: '' });
  };

  return (
    <div data-testid="contact-section" className="contact-section">
      <h2>Contact Us</h2>

      <div className="contact-details">
        <p data-testid="contact-phone">
          <strong>Phone:</strong> (555) 123-4567
        </p>
        <p data-testid="contact-email">
          <strong>Email:</strong> info@madhurirealestate.com
        </p>
        <p data-testid="contact-address">
          <strong>Address:</strong> 100 Main Street, Suite 200, Springfield, IL 62701
        </p>
      </div>

      <form onSubmit={handleSubmit} data-testid="contact-form" noValidate>
        <div className="form-group">
          <label htmlFor="contact-name">Name</label>
          <input
            id="contact-name"
            name="name"
            type="text"
            value={formData.name}
            onChange={handleChange}
            aria-describedby={errors.name ? 'name-error' : undefined}
            aria-invalid={!!errors.name}
          />
          {errors.name && (
            <span id="name-error" data-testid="name-error" className="error" role="alert">
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
            aria-describedby={errors.email ? 'email-error' : undefined}
            aria-invalid={!!errors.email}
          />
          {errors.email && (
            <span id="email-error" data-testid="email-error" className="error" role="alert">
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
            aria-describedby={errors.message ? 'message-error' : undefined}
            aria-invalid={!!errors.message}
          />
          {errors.message && (
            <span id="message-error" data-testid="message-error" className="error" role="alert">
              {errors.message}
            </span>
          )}
        </div>

        <button type="submit" data-testid="submit-button">
          Send Message
        </button>
      </form>

      {submitted && (
        <div data-testid="success-message" className="success-message" role="status">
          Thank you for your message! We will get back to you soon.
        </div>
      )}
    </div>
  );
};

export default ContactInfo;
