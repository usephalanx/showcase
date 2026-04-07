import React from 'react';
import SectionWrapper from './SectionWrapper';
import SocialIcons from './SocialIcons';
import ContactForm from './ContactForm';

export interface ContactProps {
  /** Section heading */
  heading?: string;
  /** Descriptive paragraph text */
  description?: string;
  /** Phone number to display */
  phone?: string;
  /** Email address to display */
  email?: string;
  /** Props forwarded to SocialIcons */
  socialLinks?: {
    facebook?: string;
    instagram?: string;
    linkedin?: string;
    twitter?: string;
  };
  /** Callback when the contact form is submitted */
  onFormSubmit?: (data: { name: string; email: string; phone: string; message: string }) => void;
}

const Contact: React.FC<ContactProps> = ({
  heading = 'Get In Touch',
  description = "Whether you're looking to buy, sell, or simply have questions about the local market, I'd love to hear from you. Reach out today and let's start a conversation about your real estate goals.",
  phone = '555-123-4567',
  email = 'maddie@realestate.com',
  socialLinks = {},
  onFormSubmit,
}) => {
  return (
    <SectionWrapper id="contact" background="slate">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16">
        {/* Left Column - Contact Info */}
        <div className="flex flex-col justify-center">
          <h2
            className="font-playfair text-3xl md:text-4xl lg:text-5xl font-bold text-cream-100 mb-6"
            data-testid="contact-heading"
          >
            {heading}
          </h2>

          <p
            className="text-cream-200 text-base md:text-lg leading-relaxed mb-8"
            data-testid="contact-description"
          >
            {description}
          </p>

          <div className="space-y-4 mb-8">
            {/* Phone */}
            <div className="flex items-center gap-3">
              <svg
                className="w-5 h-5 text-gold-400 flex-shrink-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
                />
              </svg>
              <a
                href={`tel:${phone.replace(/[^\d+]/g, '')}`}
                className="text-cream-100 hover:text-gold-400 transition-colors duration-200 text-base md:text-lg"
                data-testid="contact-phone"
              >
                {phone}
              </a>
            </div>

            {/* Email */}
            <div className="flex items-center gap-3">
              <svg
                className="w-5 h-5 text-gold-400 flex-shrink-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
              <a
                href={`mailto:${email}`}
                className="text-cream-100 hover:text-gold-400 transition-colors duration-200 text-base md:text-lg"
                data-testid="contact-email"
              >
                {email}
              </a>
            </div>
          </div>

          {/* Social Icons */}
          <div data-testid="contact-social-icons">
            <SocialIcons {...socialLinks} />
          </div>
        </div>

        {/* Right Column - Contact Form */}
        <div
          className="flex flex-col justify-center"
          data-testid="contact-form-wrapper"
        >
          <ContactForm onSubmit={onFormSubmit} />
        </div>
      </div>
    </SectionWrapper>
  );
};

export default Contact;
