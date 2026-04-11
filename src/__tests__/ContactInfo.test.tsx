import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import ContactInfo from '../components/ContactInfo';

/**
 * Test suite for the ContactInfo component.
 * Covers contact info display, form rendering, form validation,
 * and successful submission flow.
 */
describe('ContactInfo', () => {
  beforeEach(() => {
    render(<ContactInfo />);
  });

  describe('contact details display', () => {
    it('renders the section heading', () => {
      expect(screen.getByRole('heading', { name: /contact us/i })).toBeInTheDocument();
    });

    it('displays the phone number', () => {
      expect(screen.getByTestId('contact-phone')).toHaveTextContent('(555) 123-4567');
    });

    it('displays the email address', () => {
      expect(screen.getByTestId('contact-email')).toHaveTextContent('info@madhurirealestate.com');
    });

    it('displays the physical address', () => {
      expect(screen.getByTestId('contact-address')).toHaveTextContent(
        '100 Main Street, Suite 200, Springfield, IL 62701'
      );
    });
  });

  describe('contact form rendering', () => {
    it('renders the contact form', () => {
      expect(screen.getByTestId('contact-form')).toBeInTheDocument();
    });

    it('renders name input with label', () => {
      expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    });

    it('renders email input with label', () => {
      expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    });

    it('renders message textarea with label', () => {
      expect(screen.getByLabelText(/message/i)).toBeInTheDocument();
    });

    it('renders submit button', () => {
      expect(screen.getByTestId('submit-button')).toBeInTheDocument();
      expect(screen.getByTestId('submit-button')).toHaveTextContent(/send message/i);
    });
  });

  describe('form validation - empty submission', () => {
    it('shows all validation errors when form is submitted empty', async () => {
      const user = userEvent.setup();
      await user.click(screen.getByTestId('submit-button'));

      expect(screen.getByTestId('name-error')).toHaveTextContent('Name is required');
      expect(screen.getByTestId('email-error')).toHaveTextContent('Email is required');
      expect(screen.getByTestId('message-error')).toHaveTextContent('Message is required');
    });

    it('does not show success message on failed validation', async () => {
      const user = userEvent.setup();
      await user.click(screen.getByTestId('submit-button'));

      expect(screen.queryByTestId('success-message')).not.toBeInTheDocument();
    });
  });

  describe('form validation - invalid email', () => {
    it('shows email validation error for invalid format', async () => {
      const user = userEvent.setup();

      await user.type(screen.getByLabelText(/name/i), 'John Doe');
      await user.type(screen.getByLabelText(/email/i), 'not-an-email');
      await user.type(screen.getByLabelText(/message/i), 'Hello there');
      await user.click(screen.getByTestId('submit-button'));

      expect(screen.getByTestId('email-error')).toHaveTextContent(
        'Please enter a valid email address'
      );
      expect(screen.queryByTestId('name-error')).not.toBeInTheDocument();
      expect(screen.queryByTestId('message-error')).not.toBeInTheDocument();
    });
  });

  describe('form validation - partial submission', () => {
    it('shows error only for missing fields', async () => {
      const user = userEvent.setup();

      await user.type(screen.getByLabelText(/name/i), 'Jane Doe');
      await user.click(screen.getByTestId('submit-button'));

      expect(screen.queryByTestId('name-error')).not.toBeInTheDocument();
      expect(screen.getByTestId('email-error')).toBeInTheDocument();
      expect(screen.getByTestId('message-error')).toBeInTheDocument();
    });
  });

  describe('successful form submission', () => {
    it('shows success message when all fields are valid', async () => {
      const user = userEvent.setup();

      await user.type(screen.getByLabelText(/name/i), 'John Doe');
      await user.type(screen.getByLabelText(/email/i), 'john@example.com');
      await user.type(screen.getByLabelText(/message/i), 'I am interested in a property.');
      await user.click(screen.getByTestId('submit-button'));

      expect(screen.getByTestId('success-message')).toHaveTextContent(
        /thank you for your message/i
      );
    });

    it('clears form fields after successful submission', async () => {
      const user = userEvent.setup();

      await user.type(screen.getByLabelText(/name/i), 'John Doe');
      await user.type(screen.getByLabelText(/email/i), 'john@example.com');
      await user.type(screen.getByLabelText(/message/i), 'I am interested in a property.');
      await user.click(screen.getByTestId('submit-button'));

      expect(screen.getByLabelText(/name/i)).toHaveValue('');
      expect(screen.getByLabelText(/email/i)).toHaveValue('');
      expect(screen.getByLabelText(/message/i)).toHaveValue('');
    });

    it('does not show validation errors after successful submission', async () => {
      const user = userEvent.setup();

      await user.type(screen.getByLabelText(/name/i), 'John Doe');
      await user.type(screen.getByLabelText(/email/i), 'john@example.com');
      await user.type(screen.getByLabelText(/message/i), 'I am interested in a property.');
      await user.click(screen.getByTestId('submit-button'));

      expect(screen.queryByTestId('name-error')).not.toBeInTheDocument();
      expect(screen.queryByTestId('email-error')).not.toBeInTheDocument();
      expect(screen.queryByTestId('message-error')).not.toBeInTheDocument();
    });
  });

  describe('error clearing on input', () => {
    it('clears the name error when the user starts typing in the name field', async () => {
      const user = userEvent.setup();

      await user.click(screen.getByTestId('submit-button'));
      expect(screen.getByTestId('name-error')).toBeInTheDocument();

      await user.type(screen.getByLabelText(/name/i), 'J');
      expect(screen.queryByTestId('name-error')).not.toBeInTheDocument();
    });

    it('clears the email error when the user starts typing in the email field', async () => {
      const user = userEvent.setup();

      await user.click(screen.getByTestId('submit-button'));
      expect(screen.getByTestId('email-error')).toBeInTheDocument();

      await user.type(screen.getByLabelText(/email/i), 'j');
      expect(screen.queryByTestId('email-error')).not.toBeInTheDocument();
    });

    it('clears the message error when the user starts typing in the message field', async () => {
      const user = userEvent.setup();

      await user.click(screen.getByTestId('submit-button'));
      expect(screen.getByTestId('message-error')).toBeInTheDocument();

      await user.type(screen.getByLabelText(/message/i), 'H');
      expect(screen.queryByTestId('message-error')).not.toBeInTheDocument();
    });
  });

  describe('accessibility', () => {
    it('marks fields as aria-invalid when validation fails', async () => {
      const user = userEvent.setup();
      await user.click(screen.getByTestId('submit-button'));

      expect(screen.getByLabelText(/name/i)).toHaveAttribute('aria-invalid', 'true');
      expect(screen.getByLabelText(/email/i)).toHaveAttribute('aria-invalid', 'true');
      expect(screen.getByLabelText(/message/i)).toHaveAttribute('aria-invalid', 'true');
    });

    it('error messages have role="alert"', async () => {
      const user = userEvent.setup();
      await user.click(screen.getByTestId('submit-button'));

      const alerts = screen.getAllByRole('alert');
      expect(alerts).toHaveLength(3);
    });

    it('success message has role="status"', async () => {
      const user = userEvent.setup();

      await user.type(screen.getByLabelText(/name/i), 'John Doe');
      await user.type(screen.getByLabelText(/email/i), 'john@example.com');
      await user.type(screen.getByLabelText(/message/i), 'Hello');
      await user.click(screen.getByTestId('submit-button'));

      expect(screen.getByRole('status')).toBeInTheDocument();
    });
  });
});
