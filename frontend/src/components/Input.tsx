import React, { useId } from 'react';

export interface InputProps {
  /** Label text displayed above the input */
  label: string;
  /** Placeholder text for the input */
  placeholder?: string;
  /** Controlled value */
  value: string;
  /** Change handler */
  onChange: (value: string) => void;
  /** Input type — defaults to 'text' */
  type?: 'text' | 'email' | 'tel' | 'number' | 'textarea';
  /** HTML name attribute */
  name?: string;
  /** Whether the field is required */
  required?: boolean;
  /** Error message to display below the input */
  error?: string;
  /** Additional CSS class names */
  className?: string;
  /** Whether the input is disabled */
  disabled?: boolean;
}

const Input: React.FC<InputProps> = ({
  label,
  placeholder = '',
  value,
  onChange,
  type = 'text',
  name,
  required = false,
  error,
  className = '',
  disabled = false,
}) => {
  const generatedId = useId();
  const inputId = name ? `input-${name}` : generatedId;

  const baseClasses = [
    'block',
    'w-full',
    'rounded-lg',
    'border',
    'px-4',
    'py-3',
    'text-sm',
    'text-gray-900',
    'placeholder-gray-400',
    'bg-white',
    'transition-colors',
    'duration-200',
    'outline-none',
    disabled ? 'opacity-50 cursor-not-allowed bg-gray-50' : '',
    error
      ? 'border-red-500 focus:border-red-500 focus:ring-2 focus:ring-red-200'
      : 'border-gray-300 focus:border-blue-600 focus:ring-2 focus:ring-blue-200',
  ]
    .filter(Boolean)
    .join(' ');

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    onChange(e.target.value);
  };

  const sharedProps = {
    id: inputId,
    name,
    value,
    placeholder,
    required,
    disabled,
    onChange: handleChange,
    'aria-invalid': error ? (true as const) : undefined,
    'aria-describedby': error ? `${inputId}-error` : undefined,
  };

  return (
    <div className={`flex flex-col gap-1.5 ${className}`}>
      <label
        htmlFor={inputId}
        className="text-sm font-medium text-gray-700"
      >
        {label}
        {required && (
          <span className="ml-0.5 text-red-500" aria-hidden="true">
            *
          </span>
        )}
      </label>

      {type === 'textarea' ? (
        <textarea
          {...sharedProps}
          className={`${baseClasses} min-h-[120px] resize-y`}
          rows={4}
        />
      ) : (
        <input
          {...sharedProps}
          type={type}
          className={baseClasses}
        />
      )}

      {error && (
        <p
          id={`${inputId}-error`}
          className="text-xs text-red-600 mt-0.5"
          role="alert"
        >
          {error}
        </p>
      )}
    </div>
  );
};

export default Input;
