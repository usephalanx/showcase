import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';
import ContactInfo from '../components/ContactInfo';

describe('ContactInfo', () => {
  it('renders the contact section heading', () => {
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
      'madhuri@madhurirealestate.com'
    );
  });

  it('displays physical address', () => {
    render(<ContactInfo />);
    const addr = screen.getByTestId('contact-address');
    expect(addr).toHaveTextContent(/100 Main Street/);
    expect(addr).toHaveTextContent(/Springfield/);
  });

  it('renders the contact form with all fields', () => {
    render(<ContactInfo />);
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/phone/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/message/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /send message/i })).toBeInTheDocument();
  });

  it('validates required fields on empty submit', async () => {
    const user = userEvent.setup();
    render(<ContactInfo />);

    await user.click(screen.getByRole('button', { name: /send message/i }));

    expect(screen.getByTestId('name-error')).toHaveTextContent('Name is required');
    expect(screen.getByTestId('email-error')).toHaveTextContent('Email is required');
    expect(screen.getByTestId('message-error')).toHaveTextContent(
      'Message is required'
    );
  });

  it('validates email format', async () => {
    const user = userEvent.setup();
    render(<ContactInfo />);

    await user.type(screen.getByLabelText(/name/i), 'Test');
    await user.type(screen.getByLabelText(/email/i), 'bad-email');
    await user.type(screen.getByLabelText(/message/i), 'Test message');
    await user.click(screen.getByRole('button', { name: /send message/i }));

    expect(screen.getByTestId('email-error')).toHaveTextContent(
      'Please enter a valid email address'
    );
  });

  it('accepts valid form and shows success', async () => {
    const user = userEvent.setup();
    render(<ContactInfo />);

    await user.type(screen.getByLabelText(/name/i), 'Jane');
    await user.type(screen.getByLabelText(/email/i), 'jane@test.com');
    await user.type(screen.getByLabelText(/message/i), 'Hello!');
    await user.click(screen.getByRole('button', { name: /send message/i }));

    expect(screen.getByTestId('form-success')).toBeInTheDocument();
    expect(screen.queryByTestId('name-error')).not.toBeInTheDocument();
    expect(screen.queryByTestId('email-error')).not.toBeInTheDocument();
    expect(screen.queryByTestId('message-error')).not.toBeInTheDocument();
  });

  it('clears the form after successful submission', async () => {
    const user = userEvent.setup();
    render(<ContactInfo />);

    const nameInput = screen.getByLabelText(/name/i) as HTMLInputElement;
    const emailInput = screen.getByLabelText(/email/i) as HTMLInputElement;
    const messageInput = screen.getByLabelText(/message/i) as HTMLTextAreaElement;

    await user.type(nameInput, 'Jane');
    await user.type(emailInput, 'jane@test.com');
    await user.type(messageInput, 'Hello!');
    await user.click(screen.getByRole('button', { name: /send message/i }));

    expect(nameInput.value).toBe('');
    expect(emailInput.value).toBe('');
    expect(messageInput.value).toBe('');
  });

  it('clears field error when user types', async () => {
    const user = userEvent.setup();
    render(<ContactInfo />);

    await user.click(screen.getByRole('button', { name: /send message/i }));
    expect(screen.getByTestId('name-error')).toBeInTheDocument();

    await user.type(screen.getByLabelText(/name/i), 'A');
    expect(screen.queryByTestId('name-error')).not.toBeInTheDocument();
  });

  it('phone field is optional', async () => {
    const user = userEvent.setup();
    render(<ContactInfo />);

    await user.type(screen.getByLabelText(/name/i), 'Jane');
    await user.type(screen.getByLabelText(/email/i), 'jane@test.com');
    await user.type(screen.getByLabelText(/message/i), 'Hello!');
    await user.click(screen.getByRole('button', { name: /send message/i }));

    // Should succeed without phone
    expect(screen.getByTestId('form-success')).toBeInTheDocument();
  });
});
