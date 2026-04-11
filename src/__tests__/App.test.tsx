import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../App';
import Logo from '../components/Logo';
import CompanyName from '../components/CompanyName';

describe('App component', () => {
  test('renders the app container', () => {
    render(<App />);
    const appElement = screen.getByTestId('app');
    expect(appElement).toBeInTheDocument();
  });

  test('renders the header with banner role', () => {
    render(<App />);
    const header = screen.getByRole('banner');
    expect(header).toBeInTheDocument();
  });

  test('renders the main content area', () => {
    render(<App />);
    const main = screen.getByRole('main');
    expect(main).toBeInTheDocument();
  });

  test('renders Logo component within the header', () => {
    render(<App />);
    const logo = screen.getByTestId('logo');
    expect(logo).toBeInTheDocument();
  });

  test('renders CompanyName component within the header', () => {
    render(<App />);
    const companyName = screen.getByTestId('company-name');
    expect(companyName).toBeInTheDocument();
  });

  test('Logo appears before CompanyName in the DOM', () => {
    render(<App />);
    const header = screen.getByRole('banner');
    const children = Array.from(header.children);
    const logoIndex = children.findIndex(
      (child) => (child as HTMLElement).dataset.testid === 'logo'
    );
    const nameIndex = children.findIndex(
      (child) => (child as HTMLElement).dataset.testid === 'company-name'
    );
    expect(logoIndex).toBeLessThan(nameIndex);
    expect(logoIndex).toBeGreaterThanOrEqual(0);
    expect(nameIndex).toBeGreaterThanOrEqual(0);
  });
});

describe('Logo component', () => {
  test('renders logo image with correct alt text', () => {
    render(<Logo />);
    const img = screen.getByAltText('Madhuri Real Estate logo');
    expect(img).toBeInTheDocument();
    expect(img).toHaveAttribute('src', '/logo.svg');
  });

  test('logo image has role="img" for accessibility', () => {
    render(<Logo />);
    const img = screen.getByRole('img');
    expect(img).toBeInTheDocument();
  });

  test('logo image has width and height attributes', () => {
    render(<Logo />);
    const img = screen.getByAltText('Madhuri Real Estate logo');
    expect(img).toHaveAttribute('width', '120');
    expect(img).toHaveAttribute('height', '120');
  });

  test('logo has the correct CSS class', () => {
    render(<Logo />);
    const img = screen.getByAltText('Madhuri Real Estate logo');
    expect(img).toHaveClass('logo-image');
  });
});

describe('CompanyName component', () => {
  test('renders the company name text', () => {
    render(<CompanyName />);
    const heading = screen.getByText('Madhuri Real Estate');
    expect(heading).toBeInTheDocument();
  });

  test('company name uses an h1 heading tag', () => {
    render(<CompanyName />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent('Madhuri Real Estate');
  });

  test('company name heading has the correct CSS class', () => {
    render(<CompanyName />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toHaveClass('company-name');
  });

  test('renders the tagline subtitle', () => {
    render(<CompanyName />);
    const subtitle = screen.getByText('Your Dream Home Awaits');
    expect(subtitle).toBeInTheDocument();
  });

  test('subtitle has the correct CSS class', () => {
    render(<CompanyName />);
    const subtitle = screen.getByText('Your Dream Home Awaits');
    expect(subtitle).toHaveClass('company-name-subtitle');
  });
});
