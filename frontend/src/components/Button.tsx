import React from 'react';

export interface ButtonProps {
  /** Visual variant of the button */
  variant?: 'primary' | 'secondary' | 'outline';
  /** Button content */
  children: React.ReactNode;
  /** Click handler (ignored when href is provided) */
  onClick?: (e: React.MouseEvent<HTMLButtonElement | HTMLAnchorElement>) => void;
  /** If provided, renders an <a> tag instead of <button> */
  href?: string;
  /** Additional CSS classes */
  className?: string;
  /** Accessible label when children is not descriptive enough */
  'aria-label'?: string;
  /** Whether the button is disabled */
  disabled?: boolean;
  /** Button type attribute (only applies to <button>) */
  type?: 'button' | 'submit' | 'reset';
}

const baseClasses = [
  'inline-flex',
  'items-center',
  'justify-center',
  'px-6',
  'py-3',
  'rounded-md',
  'font-inter',
  'font-semibold',
  'text-sm',
  'tracking-wide',
  'uppercase',
  'transition-all',
  'duration-300',
  'ease-in-out',
  'transform',
  'hover:scale-105',
  'focus-visible:outline-none',
  'focus-visible:ring-2',
  'focus-visible:ring-gold',
  'focus-visible:ring-offset-2',
  'focus-visible:ring-offset-slate-900',
  'disabled:opacity-50',
  'disabled:cursor-not-allowed',
  'disabled:hover:scale-100',
].join(' ');

const variantClasses: Record<NonNullable<ButtonProps['variant']>, string> = {
  primary: [
    'bg-gold',
    'text-slate-900',
    'hover:shadow-[0_0_20px_rgba(200,169,81,0.4)]',
    'hover:bg-gold-light',
    'active:bg-gold-dark',
  ].join(' '),
  secondary: [
    'bg-transparent',
    'text-gold',
    'border-2',
    'border-gold',
    'hover:bg-gold',
    'hover:text-slate-900',
    'active:bg-gold-dark',
  ].join(' '),
  outline: [
    'bg-transparent',
    'text-slate-300',
    'border-2',
    'border-slate-500',
    'hover:border-slate-300',
    'hover:text-white',
    'active:border-slate-200',
  ].join(' '),
};

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  children,
  onClick,
  href,
  className = '',
  disabled = false,
  type = 'button',
  ...rest
}) => {
  const classes = `${baseClasses} ${variantClasses[variant]} ${className}`.trim();

  if (href && !disabled) {
    return (
      <a
        href={href}
        className={classes}
        onClick={onClick as React.MouseEventHandler<HTMLAnchorElement>}
        role="button"
        aria-label={rest['aria-label']}
      >
        {children}
      </a>
    );
  }

  return (
    <button
      type={type}
      className={classes}
      onClick={onClick as React.MouseEventHandler<HTMLButtonElement>}
      disabled={disabled}
      aria-label={rest['aria-label']}
    >
      {children}
    </button>
  );
};

export default Button;
