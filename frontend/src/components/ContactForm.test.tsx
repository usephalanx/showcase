import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ContactForm from './ContactForm';

// Minimal stubs for Input and Button if not already provided
vi.mock('./Input', () => ({
  default: (props: React.InputHTMLAttributes<HTMLInputElement>) => (
    <input data-testid={`input-${props.name}`} {...props} />
  ),
}));

vi.mock('./Button', () => ({
  default: ({ children, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) => (
    <button {...props}>{children}</button>
  ),
}));

const PROPERTY_OPTIONS = ['Sunset Villa', 'Downtown Condo', 'Lake House'];

function fillForm() {
  fireEvent.change(screen.getByTestId('input-name'), {
    target: { name: 'name', value: 'Jane Doe' },
  });
  fireEvent.change(screen.getByTestId('input-email'), {
    target: { name: 'email', value: 'jane@example.com' },
  });
  fireEvent.change(screen.getByTestId('input-phone'), {
    target: { name: 'phone', value: '555-1234' },
  });
  fireEvent.change(screen.getByRole('combobox'), {
    target: { name: 'propertyInterest', value: 'Downtown Condo' },
  });
  fireEvent.change(screen.getByPlaceholderText('Your message...'), {
    target: { name: 'message', value: 'I am interested' },
  });
}

describe('ContactForm', () => {
  it('renders without crashing', () => {
    render(<ContactForm propertyOptions={PROPERTY_OPTIONS} />);
    expect(screen.getByText('Send Message')).toBeInTheDocument();
  });

  it('displays agent name when agentName prop is provided', () => {
    render(<ContactForm agentName="John Smith" propertyOptions={PROPERTY_OPTIONS} />);
    expect(screen.getByTestId('agent-label')).toHaveTextContent('John Smith');
  });

  it('does not display agent label when agentName is not provided', () => {
    render(<ContactForm propertyOptions={PROPERTY_OPTIONS} />);
    expect(screen.queryByTestId('agent-label')).not.toBeInTheDocument();
  });

  it('pre-fills property interest when propertyTitle is provided', () => {
    render(
      <ContactForm
        propertyTitle="Sunset Villa"
        propertyOptions={PROPERTY_OPTIONS}
      />
    );
    const select = screen.getByRole('combobox') as HTMLSelectElement;
    expect(select.value).toBe('Sunset Villa');
  });

  it('shows validation errors when submitting empty form', async () => {
    render(<ContactForm propertyOptions={PROPERTY_OPTIONS} />);
    fireEvent.click(screen.getByText('Send Message'));

    const alerts = screen.getAllByRole('alert');
    expect(alerts.length).toBeGreaterThanOrEqual(4);
    expect(screen.getByText('Name is required')).toBeInTheDocument();
    expect(screen.getByText('Email is required')).toBeInTheDocument();
    expect(screen.getByText('Phone number is required')).toBeInTheDocument();
    expect(screen.getByText('Message is required')).toBeInTheDocument();
  });

  it('shows email format error for invalid email', () => {
    render(<ContactForm propertyOptions={PROPERTY_OPTIONS} />);

    fireEvent.change(screen.getByTestId('input-email'), {
      target: { name: 'email', value: 'not-an-email' },
    });
    fireEvent.click(screen.getByText('Send Message'));

    expect(screen.getByText('Please enter a valid email address')).toBeInTheDocument();
  });

  it('calls onSubmit and shows success message on valid submission', () => {
    const handleSubmit = vi.fn();
    render(
      <ContactForm
        propertyOptions={PROPERTY_OPTIONS}
        onSubmit={handleSubmit}
      />
    );

    fillForm();
    fireEvent.click(screen.getByText('Send Message'));

    expect(handleSubmit).toHaveBeenCalledTimes(1);
    expect(handleSubmit).toHaveBeenCalledWith(
      expect.objectContaining({
        name: 'Jane Doe',
        email: 'jane@example.com',
        phone: '555-1234',
        message: 'I am interested',
        propertyInterest: 'Downtown Condo',
        preferredContact: 'email',
      })
    );

    expect(screen.getByTestId('success-message')).toHaveTextContent(
      'Your message has been sent successfully!'
    );
  });

  it('allows changing preferred contact method to phone', () => {
    const handleSubmit = vi.fn();
    render(
      <ContactForm
        propertyOptions={PROPERTY_OPTIONS}
        onSubmit={handleSubmit}
      />
    );

    fillForm();
    fireEvent.click(screen.getByLabelText('Phone'));
    fireEvent.click(screen.getByText('Send Message'));

    expect(handleSubmit).toHaveBeenCalledWith(
      expect.objectContaining({ preferredContact: 'phone' })
    );
  });

  it('dismisses success message when close button is clicked', () => {
    render(<ContactForm propertyOptions={PROPERTY_OPTIONS} />);

    fillForm();
    fireEvent.click(screen.getByText('Send Message'));
    expect(screen.getByTestId('success-message')).toBeInTheDocument();

    fireEvent.click(screen.getByLabelText('Dismiss success message'));
    expect(screen.queryByTestId('success-message')).not.toBeInTheDocument();
  });

  it('clears field-level error when user types into that field', () => {
    render(<ContactForm propertyOptions={PROPERTY_OPTIONS} />);

    fireEvent.click(screen.getByText('Send Message'));
    expect(screen.getByText('Name is required')).toBeInTheDocument();

    fireEvent.change(screen.getByTestId('input-name'), {
      target: { name: 'name', value: 'A' },
    });
    expect(screen.queryByText('Name is required')).not.toBeInTheDocument();
  });

  it('renders all property options in the dropdown', () => {
    render(<ContactForm propertyOptions={PROPERTY_OPTIONS} />);
    const options = screen.getByRole('combobox').querySelectorAll('option');
    // +1 for the placeholder option
    expect(options.length).toBe(PROPERTY_OPTIONS.length + 1);
  });

  it('defaults preferred contact method to email', () => {
    render(<ContactForm propertyOptions={PROPERTY_OPTIONS} />);
    const emailRadio = screen.getByLabelText('Email') as HTMLInputElement;
    const phoneRadio = screen.getByLabelText('Phone') as HTMLInputElement;
    expect(emailRadio.checked).toBe(true);
    expect(phoneRadio.checked).toBe(false);
  });
});
