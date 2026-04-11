import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ContactInfo from '../components/ContactInfo';

/**
 * Test suite for the ContactInfo component.
 * Tests contact details display and form validation.
 */
describe('ContactInfo', () => {
  beforeEach(() => {
    render(<ContactInfo />);
  });

  describe('Contact details', () => {
    it('displays the phone number', () => {
      expect(screen.getByText('(555) 123-4567')).toBeInTheDocument();
    });

    it('displays the email address', () => {
      expect(screen.getByText('info@madhurirealestate.com')).toBeInTheDocument();
    });

    it('displays the physical address', () => {
      expect(screen.getByText(/100 Main Street/i)).toBeInTheDocument();
    });

    it('renders the section heading', () => {
      expect(screen.getByRole('heading', { name: /get in touch/i })).toBeInTheDocument();
    });
  });

  describe('Contact form', () => {
    it('renders the contact form', () => {
      expect(screen.getByTestId('contact-form')).toBeInTheDocument();
    });

    it('renders name, email, and message fields', () => {
      expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/message/i)).toBeInTheDocument();
    });

    it('renders a submit button', () => {
      expect(screen.getByRole('button', { name: /send message/i })).toBeInTheDocument();
    });

    it('shows validation errors when submitting empty form', () => {
      fireEvent.click(screen.getByRole('button', { name: /send message/i }));

      expect(screen.getByTestId('error-name')).toHaveTextContent('Name is required');
      expect(screen.getByTestId('error-email')).toHaveTextContent('Email is required');
      expect(screen.getByTestId('error-message')).toHaveTextContent('Message is required');
    });

    it('shows email format error for invalid email', () => {
      fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'John' } });
      fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'not-an-email' } });
      fireEvent.change(screen.getByLabelText(/message/i), { target: { value: 'Hello' } });
      fireEvent.click(screen.getByRole('button', { name: /send message/i }));

      expect(screen.getByTestId('error-email')).toHaveTextContent('Please enter a valid email address');
      expect(screen.queryByTestId('error-name')).not.toBeInTheDocument();
      expect(screen.queryByTestId('error-message')).not.toBeInTheDocument();
    });

    it('shows success message on valid submission', () => {
      fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'Jane Doe' } });
      fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'jane@example.com' } });
      fireEvent.change(screen.getByLabelText(/message/i), { target: { value: 'I want to buy a house.' } });
      fireEvent.click(screen.getByRole('button', { name: /send message/i }));

      expect(screen.getByTestId('form-success')).toHaveTextContent(/thank you/i);
      expect(screen.queryByTestId('error-name')).not.toBeInTheDocument();
      expect(screen.queryByTestId('error-email')).not.toBeInTheDocument();
      expect(screen.queryByTestId('error-message')).not.toBeInTheDocument();
    });

    it('clears form fields after successful submission', () => {
      fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'Jane' } });
      fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'jane@example.com' } });
      fireEvent.change(screen.getByLabelText(/message/i), { target: { value: 'Hello' } });
      fireEvent.click(screen.getByRole('button', { name: /send message/i }));

      expect((screen.getByLabelText(/name/i) as HTMLInputElement).value).toBe('');
      expect((screen.getByLabelText(/email/i) as HTMLInputElement).value).toBe('');
      expect((screen.getByLabelText(/message/i) as HTMLTextAreaElement).value).toBe('');
    });

    it('clears field error when user types in the field', () => {
      // Submit empty to trigger errors
      fireEvent.click(screen.getByRole('button', { name: /send message/i }));
      expect(screen.getByTestId('error-name')).toBeInTheDocument();

      // Type in name field
      fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'A' } });
      expect(screen.queryByTestId('error-name')).not.toBeInTheDocument();
    });
  });
});
