import React, { useState } from 'react';

/** Props for the ContactInfo component. */
interface ContactInfoProps {
  /** Phone number to display. */
  phone?: string;
  /** Email address to display. */
  email?: string;
  /** Office address to display. */
  address?: string;
}

/**
 * ContactInfo component provides clear contact information
 * and a simple contact form with basic validation.
 */
const ContactInfo: React.FC<ContactInfoProps> = ({
  phone = '(555) 123-4567',
  email = 'info@madhurirealestate.com',
  address = '100 Main Street, Suite 200, Springfield, IL 62701',
}) => {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    if (!formData.message.trim()) newErrors.message = 'Message is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) {
      setSubmitted(true);
      setFormData({ name: '', email: '', message: '' });
      setErrors({});
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <section className="section contact-section" data-testid="contact-section">
      <h2>Contact Us</h2>

      <div className="contact-info-grid">
        <div className="contact-item">
          <div>
            <p className="label">Phone</p>
            <p className="value" data-testid="contact-phone">{phone}</p>
          </div>
        </div>
        <div className="contact-item">
          <div>
            <p className="label">Email</p>
            <p className="value" data-testid="contact-email">{email}</p>
          </div>
        </div>
        <div className="contact-item">
          <div>
            <p className="label">Address</p>
            <p className="value" data-testid="contact-address">{address}</p>
          </div>
        </div>
      </div>

      {submitted && (
        <p data-testid="success-message" style={{ color: 'var(--color-success)', textAlign: 'center', marginBottom: 'var(--space-md)' }}>
          Thank you for your message! We will get back to you soon.
        </p>
      )}

      <form className="contact-form" onSubmit={handleSubmit} data-testid="contact-form" noValidate>
        <div>
          <input
            type="text"
            name="name"
            placeholder="Your Name"
            value={formData.name}
            onChange={handleChange}
            aria-label="Your Name"
          />
          {errors.name && <p className="form-error" data-testid="error-name">{errors.name}</p>}
        </div>
        <div>
          <input
            type="email"
            name="email"
            placeholder="Your Email"
            value={formData.email}
            onChange={handleChange}
            aria-label="Your Email"
          />
          {errors.email && <p className="form-error" data-testid="error-email">{errors.email}</p>}
        </div>
        <div>
          <textarea
            name="message"
            placeholder="Your Message"
            value={formData.message}
            onChange={handleChange}
            aria-label="Your Message"
          />
          {errors.message && <p className="form-error" data-testid="error-message">{errors.message}</p>}
        </div>
        <button type="submit">Send Message</button>
      </form>
    </section>
  );
};

export default ContactInfo;
