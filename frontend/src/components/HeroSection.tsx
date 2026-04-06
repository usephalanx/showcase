import React, { useState, useEffect } from 'react';

export interface HeroSectionProps {
  /** Main headline text */
  headline: string;
  /** Subheading text below the headline */
  subheading: string;
  /** Background image URL (Unsplash or any valid image URL) */
  backgroundImageUrl: string;
  /** Placeholder text for the search input */
  searchPlaceholder?: string;
  /** Label for the CTA / search button */
  ctaButtonLabel?: string;
  /** Callback when the user submits a search query */
  onSearch?: (query: string) => void;
  /** Minimum height of the hero section (CSS value) */
  minHeight?: string;
  /** Overlay opacity from 0 to 1 */
  overlayOpacity?: number;
}

const HeroSection: React.FC<HeroSectionProps> = ({
  headline,
  subheading,
  backgroundImageUrl,
  searchPlaceholder = 'Search by city, neighborhood, or ZIP...',
  ctaButtonLabel = 'Search',
  onSearch,
  minHeight = '70vh',
  overlayOpacity = 0.55,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), 100);
    return () => clearTimeout(timer);
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch?.(searchQuery);
  };

  return (
    <section
      data-testid="hero-section"
      style={{
        position: 'relative',
        minHeight,
        width: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
      }}
    >
      {/* Background Image */}
      <div
        data-testid="hero-background"
        style={{
          position: 'absolute',
          inset: 0,
          backgroundImage: `url(${backgroundImageUrl})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
          zIndex: 0,
        }}
      />

      {/* Dark Overlay */}
      <div
        data-testid="hero-overlay"
        style={{
          position: 'absolute',
          inset: 0,
          backgroundColor: `rgba(0, 0, 0, ${overlayOpacity})`,
          zIndex: 1,
        }}
      />

      {/* Content */}
      <div
        data-testid="hero-content"
        style={{
          position: 'relative',
          zIndex: 2,
          textAlign: 'center',
          padding: '2rem 1.5rem',
          maxWidth: '800px',
          width: '100%',
          opacity: isVisible ? 1 : 0,
          transform: isVisible ? 'translateY(0)' : 'translateY(30px)',
          transition: 'opacity 0.8s ease-out, transform 0.8s ease-out',
        }}
      >
        <h1
          data-testid="hero-headline"
          style={{
            color: '#ffffff',
            fontSize: 'clamp(2rem, 5vw, 3.5rem)',
            fontWeight: 700,
            margin: '0 0 1rem 0',
            lineHeight: 1.2,
            letterSpacing: '-0.02em',
            textShadow: '0 2px 8px rgba(0, 0, 0, 0.3)',
          }}
        >
          {headline}
        </h1>

        <p
          data-testid="hero-subheading"
          style={{
            color: 'rgba(255, 255, 255, 0.9)',
            fontSize: 'clamp(1rem, 2.5vw, 1.35rem)',
            margin: '0 0 2.5rem 0',
            lineHeight: 1.6,
            fontWeight: 400,
            opacity: isVisible ? 1 : 0,
            transform: isVisible ? 'translateY(0)' : 'translateY(20px)',
            transition: 'opacity 1s ease-out 0.3s, transform 1s ease-out 0.3s',
          }}
        >
          {subheading}
        </p>

        <form
          data-testid="hero-search-form"
          onSubmit={handleSubmit}
          style={{
            display: 'flex',
            gap: '0',
            maxWidth: '600px',
            margin: '0 auto',
            borderRadius: '8px',
            overflow: 'hidden',
            boxShadow: '0 4px 24px rgba(0, 0, 0, 0.25)',
            opacity: isVisible ? 1 : 0,
            transform: isVisible ? 'translateY(0)' : 'translateY(20px)',
            transition: 'opacity 1s ease-out 0.5s, transform 1s ease-out 0.5s',
          }}
        >
          <input
            data-testid="hero-search-input"
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={searchPlaceholder}
            aria-label={searchPlaceholder}
            style={{
              flex: 1,
              padding: '1rem 1.25rem',
              fontSize: '1rem',
              border: 'none',
              outline: 'none',
              backgroundColor: '#ffffff',
              color: '#1a1a2e',
              minWidth: 0,
            }}
          />
          <button
            data-testid="hero-cta-button"
            type="submit"
            style={{
              padding: '1rem 2rem',
              fontSize: '1rem',
              fontWeight: 600,
              border: 'none',
              backgroundColor: '#2563eb',
              color: '#ffffff',
              cursor: 'pointer',
              whiteSpace: 'nowrap',
              transition: 'background-color 0.2s ease',
            }}
            onMouseEnter={(e) => {
              (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#1d4ed8';
            }}
            onMouseLeave={(e) => {
              (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#2563eb';
            }}
          >
            {ctaButtonLabel}
          </button>
        </form>
      </div>
    </section>
  );
};

export default HeroSection;
