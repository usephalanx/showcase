import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import SocialIcons from './SocialIcons';

describe('SocialIcons', () => {
  it('renders without crashing', () => {
    render(<SocialIcons />);
    const container = screen.getByTestId('social-icons');
    expect(container).toBeTruthy();
  });

  it('renders both Instagram and LinkedIn icons', () => {
    render(<SocialIcons />);
    const instagram = screen.getByTestId('social-icon-instagram');
    const linkedin = screen.getByTestId('social-icon-linkedin');
    expect(instagram).toBeTruthy();
    expect(linkedin).toBeTruthy();
  });

  it('each icon link has correct target and rel attributes', () => {
    render(<SocialIcons />);
    const instagram = screen.getByTestId('social-icon-instagram');
    const linkedin = screen.getByTestId('social-icon-linkedin');

    expect(instagram.getAttribute('target')).toBe('_blank');
    expect(instagram.getAttribute('rel')).toBe('noopener noreferrer');
    expect(linkedin.getAttribute('target')).toBe('_blank');
    expect(linkedin.getAttribute('rel')).toBe('noopener noreferrer');
  });

  it('each icon link has href="#"', () => {
    render(<SocialIcons />);
    const instagram = screen.getByTestId('social-icon-instagram');
    const linkedin = screen.getByTestId('social-icon-linkedin');

    expect(instagram.getAttribute('href')).toBe('#');
    expect(linkedin.getAttribute('href')).toBe('#');
  });

  it('renders accessible aria-labels on links', () => {
    render(<SocialIcons />);
    const instagram = screen.getByLabelText('Instagram');
    const linkedin = screen.getByLabelText('LinkedIn');
    expect(instagram).toBeTruthy();
    expect(linkedin).toBeTruthy();
  });

  it('contains SVG elements inside each link', () => {
    render(<SocialIcons />);
    const instagram = screen.getByTestId('social-icon-instagram');
    const linkedin = screen.getByTestId('social-icon-linkedin');

    expect(instagram.querySelector('svg')).not.toBeNull();
    expect(linkedin.querySelector('svg')).not.toBeNull();
  });

  it('applies custom className to the container', () => {
    render(<SocialIcons className="mt-8 justify-center" />);
    const container = screen.getByTestId('social-icons');
    expect(container.className).toContain('mt-8');
    expect(container.className).toContain('justify-center');
  });

  it('renders with default classes when no className is provided', () => {
    render(<SocialIcons />);
    const container = screen.getByTestId('social-icons');
    expect(container.className).toContain('inline-flex');
    expect(container.className).toContain('items-center');
    expect(container.className).toContain('gap-4');
  });

  it('SVG icons have aria-hidden="true"', () => {
    render(<SocialIcons />);
    const instagram = screen.getByTestId('social-icon-instagram');
    const linkedin = screen.getByTestId('social-icon-linkedin');

    const instaSvg = instagram.querySelector('svg');
    const linkedSvg = linkedin.querySelector('svg');

    expect(instaSvg?.getAttribute('aria-hidden')).toBe('true');
    expect(linkedSvg?.getAttribute('aria-hidden')).toBe('true');
  });
});
