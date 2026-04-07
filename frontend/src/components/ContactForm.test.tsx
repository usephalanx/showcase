import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ContactForm from './ContactForm';

// Mock the Button component since ContactForm imports it
vi.mock('./Button', () => ({
  default: ({ label, type, variant }: { label: string; type?: string; variant?: string }) => (
    <button type={type as any || 'button'} data-variant={variant}>{label}</button>
  ),
}));

describe('ContactForm', () => {
  it('renders without crashing', () => {
    render(<ContactForm />);
    expect(screen.getByTestId('contact-form')).toBeInTheDocument();
  });

  it('renders all four input fields with default labels', () => {
    render(<ContactForm />);
    expect(screen.getByLabelText('Name')).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Phone')).toBeInTheDocument();
    expect(screen.getByLabelText('Message')).toBeInTheDocument();
  });

  it('renders custom labels when provided', () => {
    render(
      <ContactForm
        nameLabel="Full Name"
        emailLabel="Email Address"
        phoneLabel="Phone Number"
        messageLabel="Your Message"
      />
    );
    expect(screen.getByLabelText('Full Name')).toBeInTheDocument();
    expect(screen.getByLabelText('Email Address')).toBeInTheDocument();
    expect(screen.getByLabelText('Phone Number')).toBeInTheDocument();
    expect(screen.getByLabelText('Your Message')).toBeInTheDocument();
  });

  it('renders title and subtitle when provided', () => {
    render(<ContactForm title="Get In Touch" subtitle="We would love to hear from you" />);
    expect(screen.getByText('Get In Touch')).toBeInTheDocument();
    expect(screen.getByText('We would love to hear from you')).toBeInTheDocument();
  });

  it('does not render title or subtitle when not provided', () => {
    render(<ContactForm />);
    const form = screen.getByTestId('contact-form');
    expect(form.querySelector('h2')).toBeNull();
  });

  it('renders the submit button with custom text', () => {
    render(<ContactForm submitButtonText="Submit Now" />);
    expect(screen.getByText('Submit Now')).toBeInTheDocument();
  });

  it('renders the submit button with default text', () => {
    render(<ContactForm />);
    expect(screen.getByText('Send Message')).toBeInTheDocument();
  });

  it('shows validation errors when submitting empty form', () => {
    render(<ContactForm />);
    fireEvent.click(screen.getByText('Send Message'));

    const alerts = screen.getAllByRole('alert');
    expect(alerts).toHaveLength(4);
    expect(screen.getByText('Name is required')).toBeInTheDocument();
    expect(screen.getByText('Email is required')).toBeInTheDocument();
    expect(screen.getByText('Phone is required')).toBeInTheDocument();
    expect(screen.getByText('Message is required')).toBeInTheDocument();
  });

  it('shows email format error for invalid email', () => {
    render(<ContactForm />);
    fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'John' } });
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'invalid-email' } });
    fireEvent.change(screen.getByLabelText('Phone'), { target: { value: '555-1234' } });
    fireEvent.change(screen.getByLabelText('Message'), { target: { value: 'Hello' } });
    fireEvent.click(screen.getByText('Send Message'));

    expect(screen.getByText('Please enter a valid email address')).toBeInTheDocument();
  });

  it('shows success message on valid submission', () => {
    const handleSubmit = vi.fn();
    render(<ContactForm onSubmit={handleSubmit} />);

    fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'john@example.com' } });
    fireEvent.change(screen.getByLabelText('Phone'), { target: { value: '555-1234' } });
    fireEvent.change(screen.getByLabelText('Message'), { target: { value: 'Hello there' } });
    fireEvent.click(screen.getByText('Send Message'));

    expect(screen.getByTestId('contact-form-success')).toBeInTheDocument();
    expect(screen.getByText('Thank you! Your message has been sent successfully.')).toBeInTheDocument();
  });

  it('calls onSubmit callback with form data on valid submission', () => {
    const handleSubmit = vi.fn();
    render(<ContactForm onSubmit={handleSubmit} />);

    fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'john@example.com' } });
    fireEvent.change(screen.getByLabelText('Phone'), { target: { value: '555-1234' } });
    fireEvent.change(screen.getByLabelText('Message'), { target: { value: 'Hello there' } });
    fireEvent.click(screen.getByText('Send Message'));

    expect(handleSubmit).toHaveBeenCalledOnce();
    expect(handleSubmit).toHaveBeenCalledWith({
      name: 'John Doe',
      email: 'john@example.com',
      phone: '555-1234',
      message: 'Hello there',
    });
  });

  it('renders custom success message', () => {
    render(<ContactForm successMessage="Message received!" />);

    fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'Jane' } });
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'jane@test.com' } });
    fireEvent.change(screen.getByLabelText('Phone'), { target: { value: '123-4567' } });
    fireEvent.change(screen.getByLabelText('Message'), { target: { value: 'Hi' } });
    fireEvent.click(screen.getByText('Send Message'));

    expect(screen.getByText('Message received!')).toBeInTheDocument();
  });

  it('allows sending another message after success', () => {
    render(<ContactForm />);

    fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'Jane' } });
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'jane@test.com' } });
    fireEvent.change(screen.getByLabelText('Phone'), { target: { value: '123-4567' } });
    fireEvent.change(screen.getByLabelText('Message'), { target: { value: 'Hi' } });
    fireEvent.click(screen.getByText('Send Message'));

    expect(screen.getByTestId('contact-form-success')).toBeInTheDocument();

    fireEvent.click(screen.getByText('Send another message'));

    expect(screen.getByTestId('contact-form')).toBeInTheDocument();
  });

  it('uses correct input types', () => {
    render(<ContactForm />);
    expect(screen.getByLabelText('Name')).toHaveAttribute('type', 'text');
    expect(screen.getByLabelText('Email')).toHaveAttribute('type', 'email');
    expect(screen.getByLabelText('Phone')).toHaveAttribute('type', 'tel');
    expect(screen.getByLabelText('Message').tagName.toLowerCase()).toBe('textarea');
  });

  it('renders placeholders correctly', () => {
    render(
      <ContactForm
        namePlaceholder="Enter name"
        emailPlaceholder="Enter email"
        phonePlaceholder="Enter phone"
        messagePlaceholder="Enter message"
      />
    );
    expect(screen.getByPlaceholderText('Enter name')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter email')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter phone')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter message')).toBeInTheDocument();
  });
});
