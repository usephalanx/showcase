import React from 'react';

export interface LogoProps {
  /** Size variant controlling the overall dimensions */
  size?: 'sm' | 'lg';
  /** Optional additional CSS class names */
  className?: string;
}

const sizeConfig = {
  sm: { width: 140, height: 36, iconScale: 0.7, fontSize: 22, subtitleSize: 7 },
  lg: { width: 260, height: 64, iconScale: 1.2, fontSize: 40, subtitleSize: 11 },
} as const;

const GOLD = '#C9A84C';
const SLATE = '#334155';

const Logo: React.FC<LogoProps> = ({ size = 'sm', className = '' }) => {
  const config = sizeConfig[size];
  const { width, height, iconScale, fontSize, subtitleSize } = config;

  const iconWidth = 24 * iconScale;
  const iconX = 4;
  const iconCenterY = height / 2;
  const textX = iconX + iconWidth + 6;

  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label="Maddie Real Estate logo"
      className={className}
      data-testid="logo-svg"
    >
      <title>Maddie Real Estate</title>

      {/* House / Key Icon */}
      <g
        transform={`translate(${iconX}, ${iconCenterY - 12 * iconScale}) scale(${iconScale})`}
        data-testid="logo-icon"
      >
        {/* House body */}
        <path
          d="M12 2L2 10h3v10h5v-6h4v6h5V10h3L12 2z"
          fill={GOLD}
          stroke={SLATE}
          strokeWidth="0.5"
        />
        {/* Key overlay (small key shape at bottom-right of house) */}
        <g transform="translate(15, 14)">
          <circle
            cx="3"
            cy="3"
            r="2.5"
            fill="none"
            stroke={SLATE}
            strokeWidth="1"
          />
          <line
            x1="5.2"
            y1="3"
            x2="9"
            y2="3"
            stroke={SLATE}
            strokeWidth="1"
            strokeLinecap="round"
          />
          <line
            x1="7.5"
            y1="3"
            x2="7.5"
            y2="5"
            stroke={SLATE}
            strokeWidth="1"
            strokeLinecap="round"
          />
          <line
            x1="9"
            y1="3"
            x2="9"
            y2="5"
            stroke={SLATE}
            strokeWidth="1"
            strokeLinecap="round"
          />
        </g>
      </g>

      {/* "Maddie" text in elegant serif style */}
      <text
        x={textX}
        y={height / 2 - (subtitleSize > 8 ? 4 : 2)}
        fontFamily="'Playfair Display', 'Georgia', 'Times New Roman', serif"
        fontSize={fontSize}
        fontWeight="600"
        fill={SLATE}
        dominantBaseline="central"
        letterSpacing="1.5"
        data-testid="logo-text"
      >
        Maddie
      </text>

      {/* Subtitle / tagline */}
      <text
        x={textX}
        y={height / 2 + fontSize / 2 + (subtitleSize > 8 ? 4 : 2)}
        fontFamily="'Inter', 'Helvetica Neue', Arial, sans-serif"
        fontSize={subtitleSize}
        fontWeight="400"
        fill={GOLD}
        letterSpacing="2.5"
        textTransform="uppercase"
        data-testid="logo-subtitle"
      >
        {'REAL ESTATE'}
      </text>

      {/* Gold accent line under the text */}
      <line
        x1={textX}
        y1={height - 4}
        x2={textX + (width - textX) * 0.6}
        y2={height - 4}
        stroke={GOLD}
        strokeWidth="1"
        opacity="0.6"
      />
    </svg>
  );
};

export default Logo;
