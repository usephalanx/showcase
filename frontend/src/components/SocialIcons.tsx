import React from 'react';

export interface SocialIconsProps {
  /** Additional CSS class names for layout customization (e.g., flex direction, gap overrides) */
  className?: string;
}

/**
 * SocialIcons renders inline SVG icons for Instagram and LinkedIn.
 * Each icon is wrapped in an anchor tag and transitions to gold on hover.
 */
const SocialIcons: React.FC<SocialIconsProps> = ({ className = '' }) => {
  const iconStyle: React.CSSProperties = {
    width: 24,
    height: 24,
    display: 'block',
  };

  const linkBaseClasses =
    'inline-flex items-center justify-center text-slate-600 transition-colors duration-300 hover:text-[#C8A951] focus:text-[#C8A951] focus:outline-none';

  return (
    <div
      className={`inline-flex items-center gap-4 ${className}`.trim()}
      data-testid="social-icons"
    >
      {/* Instagram */}
      <a
        href="#"
        target="_blank"
        rel="noopener noreferrer"
        className={linkBaseClasses}
        aria-label="Instagram"
        data-testid="social-icon-instagram"
      >
        <svg
          style={iconStyle}
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <rect x="2" y="2" width="20" height="20" rx="5" ry="5" />
          <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" />
          <line x1="17.5" y1="6.5" x2="17.51" y2="6.5" />
        </svg>
      </a>

      {/* LinkedIn */}
      <a
        href="#"
        target="_blank"
        rel="noopener noreferrer"
        className={linkBaseClasses}
        aria-label="LinkedIn"
        data-testid="social-icon-linkedin"
      >
        <svg
          style={iconStyle}
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z" />
          <rect x="2" y="9" width="4" height="12" />
          <circle cx="4" cy="4" r="2" />
        </svg>
      </a>
    </div>
  );
};

export default SocialIcons;
