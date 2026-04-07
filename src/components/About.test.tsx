import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import About, { AboutProps, TrustBadgeData } from './About';

const defaultBadges: TrustBadgeData[] = [
  { icon: '🏠', label: 'Licensed Agent' },
  { icon: '🏡', label: '200+ Homes Sold' },
  { icon: '⭐', label: '5★ Rated' },
];

const defaultProps: AboutProps = {
  sectionLabel: 'About Maddie',
  bioText:
    'Maddie is a dedicated real estate professional with over a decade of experience helping families find their dream homes.',
  trustBadges: defaultBadges,
};

describe('About', () => {
  it('renders without crashing', () => {
    const { container } = render(<About {...defaultProps} />);
    expect(container).toBeTruthy();
  });

  it('renders the section with the correct id', () => {
    const { container } = render(<About {...defaultProps} />);
    const section = container.querySelector('section#about');
    expect(section).toBeTruthy();
  });

  it('renders a custom sectionId when provided', () => {
    const { container } = render(
      <About {...defaultProps} sectionId="profile" />
    );
    const section = container.querySelector('section#profile');
    expect(section).toBeTruthy();
  });

  it('renders the section label text', () => {
    render(<About {...defaultProps} />);
    expect(screen.getByText('About Maddie')).toBeTruthy();
  });

  it('renders the bio paragraph text', () => {
    render(<About {...defaultProps} />);
    const bio = screen.getByTestId('bio-text');
    expect(bio.textContent).toBe(defaultProps.bioText);
  });

  it('renders all trust badges', () => {
    render(<About {...defaultProps} />);
    expect(screen.getByText('Licensed Agent')).toBeTruthy();
    expect(screen.getByText('200+ Homes Sold')).toBeTruthy();
    expect(screen.getByText('5★ Rated')).toBeTruthy();
  });

  it('renders the trust badges container', () => {
    render(<About {...defaultProps} />);
    const badgesContainer = screen.getByTestId('trust-badges');
    expect(badgesContainer.children.length).toBe(3);
  });

  it('renders the avatar placeholder when no image URL is provided', () => {
    render(<About {...defaultProps} />);
    const placeholder = screen.getByTestId('avatar-placeholder');
    expect(placeholder).toBeTruthy();
  });

  it('renders the gold gradient border on the avatar', () => {
    render(<About {...defaultProps} />);
    const border = screen.getByTestId('avatar-border');
    expect(border.style.background).toContain('#C8A951');
  });

  it('renders an image when avatarImageUrl is provided', () => {
    render(
      <About
        {...defaultProps}
        avatarImageUrl="https://example.com/headshot.jpg"
        avatarAlt="Maddie headshot"
      />
    );
    const img = screen.getByAlt('Maddie headshot');
    expect(img).toBeTruthy();
    expect(img.getAttribute('src')).toBe('https://example.com/headshot.jpg');
  });

  it('does not render placeholder when avatarImageUrl is given', () => {
    render(
      <About
        {...defaultProps}
        avatarImageUrl="https://example.com/headshot.jpg"
      />
    );
    expect(screen.queryByTestId('avatar-placeholder')).toBeNull();
  });

  it('renders badge icons as role=img with accessible labels', () => {
    render(<About {...defaultProps} />);
    const badgeIcons = screen.getAllByRole('img');
    expect(badgeIcons.length).toBe(3);
    expect(badgeIcons[0].getAttribute('aria-label')).toBe('Licensed Agent');
  });

  it('handles empty trust badges array gracefully', () => {
    render(<About {...defaultProps} trustBadges={[]} />);
    const badgesContainer = screen.getByTestId('trust-badges');
    expect(badgesContainer.children.length).toBe(0);
  });
});
