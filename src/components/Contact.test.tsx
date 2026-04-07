import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import Contact from './Contact';

// Mock child components to isolate Contact tests
vi.mock('./SectionWrapper', () => ({
  default: ({ children, id, background }: { children: React.ReactNode; id: string; background: string }) => (
    <section data-testid="section-wrapper" data-id={id} data-background={background}>
      {children}
    </section>
  ),
}));

vi.mock('./SocialIcons', () => ({
  default: (props: Record<string, string>) => (
    <div data-testid="social-icons" data-props={JSON.stringify(props)} />
  ),
}));

vi.mock('./ContactForm', () => ({
  default: ({ onSubmit }: { onSubmit?: Function }) => (
    <form data-testid="contact-form" data-has-submit={!!onSubmit ? 'true' : 'false'} />
  ),
}));

describe('Contact', () => {
  it('renders without crashing', () => {
    render(<Contact />);
    expect(screen.getByTestId('section-wrapper')).toBeInTheDocument();
  });

  it('uses SectionWrapper with id="contact" and slate background', () => {
    render(<Contact />);
    const wrapper = screen.getByTestId('section-wrapper');
    expect(wrapper).toHaveAttribute('data-id', 'contact');
    expect(wrapper).toHaveAttribute('data-background', 'slate');
  });

  it('renders the default heading', () => {
    render(<Contact />);
    expect(screen.getByTestId('contact-heading')).toHaveTextContent('Get In Touch');
  });

  it('renders a custom heading when provided', () => {
    render(<Contact heading="Contact Me" />);
    expect(screen.getByTestId('contact-heading')).toHaveTextContent('Contact Me');
  });

  it('renders the default description', () => {
    render(<Contact />);
    const desc = screen.getByTestId('contact-description');
    expect(desc).toBeInTheDocument();
    expect(desc.textContent).toContain('looking to buy, sell');
  });

  it('renders a custom description when provided', () => {
    render(<Contact description="Custom contact description" />);
    expect(screen.getByTestId('contact-description')).toHaveTextContent('Custom contact description');
  });

  it('renders the default phone number', () => {
    render(<Contact />);
    const phoneEl = screen.getByTestId('contact-phone');
    expect(phoneEl).toHaveTextContent('555-123-4567');
    expect(phoneEl).toHaveAttribute('href', 'tel:5551234567');
  });

  it('renders a custom phone number when provided', () => {
    render(<Contact phone="800-555-0000" />);
    const phoneEl = screen.getByTestId('contact-phone');
    expect(phoneEl).toHaveTextContent('800-555-0000');
    expect(phoneEl).toHaveAttribute('href', 'tel:8005550000');
  });

  it('renders the default email address', () => {
    render(<Contact />);
    const emailEl = screen.getByTestId('contact-email');
    expect(emailEl).toHaveTextContent('maddie@realestate.com');
    expect(emailEl).toHaveAttribute('href', 'mailto:maddie@realestate.com');
  });

  it('renders a custom email when provided', () => {
    render(<Contact email="custom@test.com" />);
    const emailEl = screen.getByTestId('contact-email');
    expect(emailEl).toHaveTextContent('custom@test.com');
    expect(emailEl).toHaveAttribute('href', 'mailto:custom@test.com');
  });

  it('renders the SocialIcons component', () => {
    render(<Contact />);
    expect(screen.getByTestId('social-icons')).toBeInTheDocument();
  });

  it('passes socialLinks to SocialIcons', () => {
    const links = { facebook: 'https://facebook.com/test', instagram: 'https://instagram.com/test' };
    render(<Contact socialLinks={links} />);
    const iconsEl = screen.getByTestId('social-icons');
    const passedProps = JSON.parse(iconsEl.getAttribute('data-props') || '{}');
    expect(passedProps.facebook).toBe('https://facebook.com/test');
    expect(passedProps.instagram).toBe('https://instagram.com/test');
  });

  it('renders the ContactForm component', () => {
    render(<Contact />);
    expect(screen.getByTestId('contact-form')).toBeInTheDocument();
  });

  it('passes onFormSubmit callback to ContactForm', () => {
    const handleSubmit = vi.fn();
    render(<Contact onFormSubmit={handleSubmit} />);
    const formEl = screen.getByTestId('contact-form');
    expect(formEl).toHaveAttribute('data-has-submit', 'true');
  });

  it('renders without onFormSubmit callback', () => {
    render(<Contact />);
    const formEl = screen.getByTestId('contact-form');
    expect(formEl).toHaveAttribute('data-has-submit', 'false');
  });

  it('renders both columns (info and form)', () => {
    render(<Contact />);
    expect(screen.getByTestId('contact-social-icons')).toBeInTheDocument();
    expect(screen.getByTestId('contact-form-wrapper')).toBeInTheDocument();
  });
});
