import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';
import { ContactInfo } from '../components/ContactInfo';

describe('ContactInfo', () => {
  it('renders the section heading', () => {
    render(<ContactInfo />);
    expect(screen.getByText('Contact Us')).toBeInTheDocument();
  });

  it('displays phone number', () => {
    render(<ContactInfo />);
    expect(screen.getByTestId('contact-phone')).toHaveTextContent('(555) 123-4567');
  });

  it('displays email address', () => {
    render(<ContactInfo />);
    expect(screen.getByTestId('contact-email')).toHaveTextContent(
      'info@madhurirealestate.com',
    );
  });

  it('displays physical address', () => {
    render(<ContactInfo />);
    expect(screen.getByTestId('contact-address')).toHaveTextContent(
      '100 Main Street, Suite 200, Springfield, IL 62701',
    );
  });

  it('renders the contact form', () => {
    render(<ContactInfo />);
    expect(screen.getByTestId('contact-form')).toBeInTheDocument();
  });

  it('renders name, email, and message fields', () => {
    render(<ContactInfo />);
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/message/i)).toBeInTheDocument();
  });

  it('shows validation errors when submitting empty form', async () => {
    const user = userEvent.setup();
    render(<ContactInfo />);

    const submitBtn = screen.getByRole('button', { name: /send message/i });
    await user.click(submitBtn);

    expect(screen.getByTestId('error-name')).toHaveTextContent('Name is required');
    expect(screen.getByTestId('error-email')).toHaveTextContent('Email is required');
    expect(screen.getByTestId('error-message')).toHaveTextContent(
      'Message is required',
    );
  });

  it('shows email validation error for invalid email', async () => {
    const user = userEvent.setup();
    render(<ContactInfo />);

    await user.type(screen.getByLabelText(/name/i), 'John Doe');
    await user.type(screen.getByLabelText(/email/i), 'invalid-email');
    await user.type(screen.getByLabelText(/message/i), 'Hello there');

    const submitBtn = screen.getByRole('button', { name: /send message/i });
    await user.click(submitBtn);

    expect(screen.getByTestId('error-email')).toHaveTextContent(
      'Please enter a valid email address',
    );
  });

  it('shows success message on valid form submission', async () => {
    const user = userEvent.setup();
    render(<ContactInfo />);

    await user.type(screen.getByLabelText(/name/i), 'John Doe');
    await user.type(screen.getByLabelText(/email/i), 'john@example.com');
    await user.type(screen.getByLabelText(/message/i), 'I am interested in a property');

    const submitBtn = screen.getByRole('button', { name: /send message/i });
    await user.click(submitBtn);

    expect(screen.getByTestId('form-success')).toBeInTheDocument();
    expect(
      screen.getByText(/thank you for your message/i),
    ).toBeInTheDocument();
  });

  it('clears form fields after successful submission', async () => {
    const user = userEvent.setup();
    render(<ContactInfo />);

    const nameInput = screen.getByLabelText(/name/i) as HTMLInputElement;
    const emailInput = screen.getByLabelText(/email/i) as HTMLInputElement;
    const messageInput = screen.getByLabelText(/message/i) as HTMLTextAreaElement;

    await user.type(nameInput, 'John Doe');
    await user.type(emailInput, 'john@example.com');
    await user.type(messageInput, 'Hello');

    const submitBtn = screen.getByRole('button', { name: /send message/i });
    await user.click(submitBtn);

    expect(nameInput.value).toBe('');
    expect(emailInput.value).toBe('');
    expect(messageInput.value).toBe('');
  });
});
