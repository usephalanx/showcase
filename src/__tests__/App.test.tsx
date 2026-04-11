import React from 'react';
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';
import App from '../App';

describe('App', () => {
  it('renders the app container', () => {
    render(<App />);
    expect(screen.getByTestId('app-container')).toBeInTheDocument();
  });

  it('renders all main sections in correct order', () => {
    render(<App />);
    const container = screen.getByTestId('app-container');
    const sections = container.children;

    expect(sections.length).toBe(5);
    expect(sections[0]).toHaveAttribute('data-testid', 'logo-section');
    expect(sections[1]).toHaveAttribute('data-testid', 'company-name-section');
    expect(sections[2]).toHaveAttribute('data-testid', 'profile-section');
    expect(sections[3]).toHaveAttribute('data-testid', 'recent-sales-section');
    expect(sections[4]).toHaveAttribute('data-testid', 'contact-section');
  });

  it('renders the Logo section with an image', () => {
    render(<App />);
    const logoSection = screen.getByTestId('logo-section');
    const img = within(logoSection).getByRole('img');
    expect(img).toHaveAttribute('alt', 'Madhuri Real Estate Logo');
  });

  it('renders the CompanyName section with heading', () => {
    render(<App />);
    expect(screen.getByText('Madhuri Real Estate')).toBeInTheDocument();
    expect(
      screen.getByText('Your Trusted Partner in Finding the Perfect Home')
    ).toBeInTheDocument();
  });

  it('renders the Profile section with image and bio', () => {
    render(<App />);
    const profileSection = screen.getByTestId('profile-section');
    expect(within(profileSection).getByText('Madhuri Sharma')).toBeInTheDocument();
    expect(
      within(profileSection).getByText('Senior Real Estate Agent')
    ).toBeInTheDocument();
    expect(
      within(profileSection).getByRole('img', { name: /Madhuri/i })
    ).toBeInTheDocument();
  });

  it('renders the RecentSales section with sale cards', () => {
    render(<App />);
    const salesSection = screen.getByTestId('recent-sales-section');
    expect(within(salesSection).getByText('Recent Sales')).toBeInTheDocument();
    const cards = within(salesSection).getAllByTestId('sale-card');
    expect(cards.length).toBeGreaterThan(0);
  });

  it('renders the ContactInfo section with contact details', () => {
    render(<App />);
    const contactSection = screen.getByTestId('contact-section');
    expect(within(contactSection).getByText('Contact Us')).toBeInTheDocument();
    expect(screen.getByTestId('contact-phone')).toHaveTextContent('(555) 123-4567');
    expect(screen.getByTestId('contact-email')).toHaveTextContent(
      'madhuri@madhurirealestate.com'
    );
    expect(screen.getByTestId('contact-address')).toBeInTheDocument();
  });

  it('renders the contact form', () => {
    render(<App />);
    expect(screen.getByTestId('contact-form')).toBeInTheDocument();
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/message/i)).toBeInTheDocument();
  });
});

describe('Profile component', () => {
  it('displays profile image with correct alt text', () => {
    render(<App />);
    const img = screen.getByAlt('Madhuri - Real Estate Agent');
    expect(img).toBeInTheDocument();
    expect(img).toHaveClass('profile-image');
  });

  it('displays agent name and role', () => {
    render(<App />);
    expect(screen.getByText('Madhuri Sharma')).toBeInTheDocument();
    expect(screen.getByText('Senior Real Estate Agent')).toBeInTheDocument();
  });

  it('displays bio text', () => {
    render(<App />);
    expect(
      screen.getByText(/With over 15 years of experience/i)
    ).toBeInTheDocument();
  });
});

describe('ContactInfo component', () => {
  it('displays phone, email, and address', () => {
    render(<App />);
    expect(screen.getByTestId('contact-phone')).toHaveTextContent('(555) 123-4567');
    expect(screen.getByTestId('contact-email')).toHaveTextContent(
      'madhuri@madhurirealestate.com'
    );
    expect(screen.getByTestId('contact-address')).toBeInTheDocument();
  });

  it('shows validation errors when submitting empty form', async () => {
    const user = userEvent.setup();
    render(<App />);

    const submitButton = screen.getByRole('button', { name: /send message/i });
    await user.click(submitButton);

    expect(screen.getByTestId('name-error')).toHaveTextContent('Name is required');
    expect(screen.getByTestId('email-error')).toHaveTextContent('Email is required');
    expect(screen.getByTestId('message-error')).toHaveTextContent(
      'Message is required'
    );
  });

  it('shows email validation error for invalid email', async () => {
    const user = userEvent.setup();
    render(<App />);

    const nameInput = screen.getByLabelText(/name/i);
    const emailInput = screen.getByLabelText(/email/i);
    const messageInput = screen.getByLabelText(/message/i);
    const submitButton = screen.getByRole('button', { name: /send message/i });

    await user.type(nameInput, 'John Doe');
    await user.type(emailInput, 'notavalidemail');
    await user.type(messageInput, 'Hello there');
    await user.click(submitButton);

    expect(screen.getByTestId('email-error')).toHaveTextContent(
      'Please enter a valid email address'
    );
    expect(screen.queryByTestId('name-error')).not.toBeInTheDocument();
    expect(screen.queryByTestId('message-error')).not.toBeInTheDocument();
  });

  it('shows success message on valid submission', async () => {
    const user = userEvent.setup();
    render(<App />);

    const nameInput = screen.getByLabelText(/name/i);
    const emailInput = screen.getByLabelText(/email/i);
    const messageInput = screen.getByLabelText(/message/i);
    const submitButton = screen.getByRole('button', { name: /send message/i });

    await user.type(nameInput, 'John Doe');
    await user.type(emailInput, 'john@example.com');
    await user.type(messageInput, 'I am interested in a property.');
    await user.click(submitButton);

    expect(screen.getByTestId('form-success')).toHaveTextContent(
      'Thank you! Your message has been sent successfully.'
    );
    expect(screen.queryByTestId('name-error')).not.toBeInTheDocument();
    expect(screen.queryByTestId('email-error')).not.toBeInTheDocument();
    expect(screen.queryByTestId('message-error')).not.toBeInTheDocument();
  });

  it('clears form fields after successful submission', async () => {
    const user = userEvent.setup();
    render(<App />);

    const nameInput = screen.getByLabelText(/name/i) as HTMLInputElement;
    const emailInput = screen.getByLabelText(/email/i) as HTMLInputElement;
    const messageInput = screen.getByLabelText(/message/i) as HTMLTextAreaElement;
    const submitButton = screen.getByRole('button', { name: /send message/i });

    await user.type(nameInput, 'John Doe');
    await user.type(emailInput, 'john@example.com');
    await user.type(messageInput, 'Hello');
    await user.click(submitButton);

    expect(nameInput.value).toBe('');
    expect(emailInput.value).toBe('');
    expect(messageInput.value).toBe('');
  });

  it('clears field error when user starts typing', async () => {
    const user = userEvent.setup();
    render(<App />);

    const submitButton = screen.getByRole('button', { name: /send message/i });
    await user.click(submitButton);

    expect(screen.getByTestId('name-error')).toBeInTheDocument();

    const nameInput = screen.getByLabelText(/name/i);
    await user.type(nameInput, 'J');

    expect(screen.queryByTestId('name-error')).not.toBeInTheDocument();
  });
});
