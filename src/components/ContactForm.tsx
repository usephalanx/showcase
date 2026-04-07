import React, { useState } from 'react';
import Button from './Button';

export interface ContactFormProps {
  /** Heading displayed above the form */
  title?: string;
  /** Subheading or description text */
  subtitle?: string;
  /** Label for the name field */
  nameLabel?: string;
  /** Placeholder for the name field */
  namePlaceholder?: string;
  /** Label for the email field */
  emailLabel?: string;
  /** Placeholder for the email field */
  emailPlaceholder?: string;
  /** Label for the phone field */
  phoneLabel?: string;
  /** Placeholder for the phone field */
  phonePlaceholder?: string;
  /** Label for the message field */
  messageLabel?: string;
  /** Placeholder for the message field */
  messagePlaceholder?: string;
  /** Text displayed on the submit button */
  submitButtonText?: string;
  /** Success message shown after successful submission */
  successMessage?: string;
  /** Optional callback fired on valid submission with form data */
  onSubmit?: (data: { name: string; email: string; phone: string; message: string }) => void;
}

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const ContactForm: React.FC<ContactFormProps> = ({
  title,
  subtitle,
  nameLabel = 'Name',
  namePlaceholder = 'Your full name',
  emailLabel = 'Email',
  emailPlaceholder = 'you@example.com',
  phoneLabel = 'Phone',
  phonePlaceholder = '(555) 123-4567',
  messageLabel = 'Message',
  messagePlaceholder = 'How can I help you?',
  submitButtonText = 'Send Message',
  successMessage = 'Thank you! Your message has been sent successfully.',
  onSubmit,
}) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [message, setMessage] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);

  const validate = (): Record<string, string> => {
    const errs: Record<string, string> = {};
    if (!name.trim()) errs.name = 'Name is required';
    if (!email.trim()) {
      errs.email = 'Email is required';
    } else if (!EMAIL_REGEX.test(email)) {
      errs.email = 'Please enter a valid email address';
    }
    if (!phone.trim()) errs.phone = 'Phone is required';
    if (!message.trim()) errs.message = 'Message is required';
    return errs;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const validationErrors = validate();
    setErrors(validationErrors);

    if (Object.keys(validationErrors).length === 0) {
      onSubmit?.({ name: name.trim(), email: email.trim(), phone: phone.trim(), message: message.trim() });
      setSubmitted(true);
      setName('');
      setEmail('');
      setPhone('');
      setMessage('');
    }
  };

  const inputClasses =
    'w-full rounded-md border border-gray-300 bg-[#FFFDF7] px-4 py-3 text-slate-800 placeholder-slate-400 transition-all duration-200 focus:border-[#C8A951] focus:outline-none focus:ring-2 focus:ring-[#C8A951]/50';
  const errorClasses = 'mt-1 text-sm text-red-600';

  if (submitted) {
    return (
      <div data-testid="contact-form-success" className="rounded-lg bg-[#FFFDF7] p-8 text-center">
        <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-100">
          <svg className="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <p className="text-lg font-medium text-slate-800">{successMessage}</p>
        <button
          type="button"
          onClick={() => setSubmitted(false)}
          className="mt-4 text-sm text-[#C8A951] underline hover:text-[#D4B968]"
        >
          Send another message
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} noValidate data-testid="contact-form" className="space-y-5">
      {title && <h2 className="font-playfair text-3xl font-bold text-slate-800">{title}</h2>}
      {subtitle && <p className="text-slate-600">{subtitle}</p>}

      <div>
        <label htmlFor="contact-name" className="mb-1 block text-sm font-medium text-slate-700">{nameLabel}</label>
        <input id="contact-name" type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder={namePlaceholder} className={inputClasses} aria-required="true" />
        {errors.name && <p className={errorClasses} role="alert">{errors.name}</p>}
      </div>

      <div>
        <label htmlFor="contact-email" className="mb-1 block text-sm font-medium text-slate-700">{emailLabel}</label>
        <input id="contact-email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder={emailPlaceholder} className={inputClasses} aria-required="true" />
        {errors.email && <p className={errorClasses} role="alert">{errors.email}</p>}
      </div>

      <div>
        <label htmlFor="contact-phone" className="mb-1 block text-sm font-medium text-slate-700">{phoneLabel}</label>
        <input id="contact-phone" type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder={phonePlaceholder} className={inputClasses} aria-required="true" />
        {errors.phone && <p className={errorClasses} role="alert">{errors.phone}</p>}
      </div>

      <div>
        <label htmlFor="contact-message" className="mb-1 block text-sm font-medium text-slate-700">{messageLabel}</label>
        <textarea id="contact-message" rows={5} value={message} onChange={(e) => setMessage(e.target.value)} placeholder={messagePlaceholder} className={`${inputClasses} resize-vertical`} aria-required="true" />
        {errors.message && <p className={errorClasses} role="alert">{errors.message}</p>}
      </div>

      <div>
        <Button variant="primary" type="submit">{submitButtonText}</Button>
      </div>
    </form>
  );
};

export default ContactForm;
