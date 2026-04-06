import React from 'react';

export type BadgeVariant = 'featured' | 'new' | 'sale' | 'rent' | 'default';

export interface BadgeProps {
  /** The text content displayed inside the badge */
  text: string;
  /** Visual variant that determines the color scheme */
  variant?: BadgeVariant;
  /** Additional CSS classes to merge with the badge */
  className?: string;
}

const variantStyles: Record<BadgeVariant, string> = {
  featured:
    'bg-amber-100 text-amber-800 border border-amber-300',
  new:
    'bg-emerald-100 text-emerald-800 border border-emerald-300',
  sale:
    'bg-blue-100 text-blue-800 border border-blue-300',
  rent:
    'bg-purple-100 text-purple-800 border border-purple-300',
  default:
    'bg-gray-100 text-gray-800 border border-gray-300',
};

const Badge: React.FC<BadgeProps> = ({
  text,
  variant = 'default',
  className = '',
}) => {
  const baseStyles =
    'inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold leading-tight whitespace-nowrap';
  const colorStyles = variantStyles[variant] || variantStyles.default;

  return (
    <span
      className={`${baseStyles} ${colorStyles}${className ? ` ${className}` : ''}`}
      data-testid="badge"
    >
      {text}
    </span>
  );
};

export default Badge;
