import React from 'react';

export interface ButtonProps {
  /** Visual style variant */
  variant?: 'primary' | 'secondary' | 'ghost';
  /** Button size */
  size?: 'sm' | 'md' | 'lg';
  /** Button content */
  children: React.ReactNode;
  /** Click handler */
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  /** Additional CSS classes */
  className?: string;
  /** Whether the button is disabled */
  disabled?: boolean;
  /** HTML button type attribute */
  type?: 'button' | 'submit' | 'reset';
}

const variantClasses: Record<NonNullable<ButtonProps['variant']>, string> = {
  primary: [
    'bg-indigo-700 text-white',
    'hover:bg-indigo-800',
    'focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2',
    'active:bg-indigo-900',
    'disabled:bg-indigo-300 disabled:cursor-not-allowed',
    'shadow-md hover:shadow-lg',
  ].join(' '),
  secondary: [
    'bg-transparent text-indigo-700 border-2 border-indigo-700',
    'hover:bg-indigo-50 hover:border-indigo-800 hover:text-indigo-800',
    'focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2',
    'active:bg-indigo-100',
    'disabled:border-indigo-300 disabled:text-indigo-300 disabled:cursor-not-allowed disabled:hover:bg-transparent',
  ].join(' '),
  ghost: [
    'bg-transparent text-indigo-700',
    'hover:bg-indigo-50 hover:text-indigo-800',
    'focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2',
    'active:bg-indigo-100',
    'disabled:text-indigo-300 disabled:cursor-not-allowed disabled:hover:bg-transparent',
  ].join(' '),
};

const sizeClasses: Record<NonNullable<ButtonProps['size']>, string> = {
  sm: 'px-3 py-1.5 text-sm font-medium rounded',
  md: 'px-5 py-2.5 text-base font-semibold rounded-md',
  lg: 'px-7 py-3.5 text-lg font-semibold rounded-lg',
};

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  children,
  onClick,
  className = '',
  disabled = false,
  type = 'button',
}) => {
  const baseClasses =
    'inline-flex items-center justify-center transition-all duration-200 ease-in-out tracking-wide';

  const combinedClasses = [
    baseClasses,
    variantClasses[variant],
    sizeClasses[size],
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <button
      type={type}
      className={combinedClasses}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export default Button;
