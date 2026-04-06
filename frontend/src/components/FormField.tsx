import React from 'react';

/**
 * Shared props for all form field variants.
 */
export interface FormFieldBaseProps {
  /** Visible label rendered above the field. */
  label: string;
  /** HTML name attribute for the field. */
  name?: string;
  /** Placeholder text shown when the field is empty. */
  placeholder?: string;
  /** Current controlled value. */
  value: string;
  /** Whether the field is disabled. */
  disabled?: boolean;
  /** Whether the field is required. */
  required?: boolean;
  /** Error message displayed below the field. Empty/undefined means no error. */
  error?: string;
  /** Additional CSS class names applied to the outermost wrapper. */
  className?: string;
  /** Unique id for the input element (also used by the label's htmlFor). */
  id?: string;
}

export interface InputProps extends FormFieldBaseProps {
  /** HTML input type (text, email, password, number, etc.). Defaults to "text". */
  type?: string;
  /** Change handler receiving the new value. */
  onChange: (value: string) => void;
  /** Optional blur handler. */
  onBlur?: () => void;
}

export interface TextAreaProps extends FormFieldBaseProps {
  /** Change handler receiving the new value. */
  onChange: (value: string) => void;
  /** Optional blur handler. */
  onBlur?: () => void;
  /** Number of visible text rows. Defaults to 4. */
  rows?: number;
}

const baseWrapperStyle: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: '4px',
  width: '100%',
};

const labelStyle: React.CSSProperties = {
  fontSize: '14px',
  fontWeight: 600,
  color: '#334155',
  userSelect: 'none',
};

const labelErrorStyle: React.CSSProperties = {
  ...labelStyle,
  color: '#dc2626',
};

const fieldBaseStyle: React.CSSProperties = {
  width: '100%',
  padding: '10px 12px',
  fontSize: '14px',
  lineHeight: '1.5',
  color: '#1e293b',
  backgroundColor: '#ffffff',
  border: '1px solid #cbd5e1',
  borderRadius: '6px',
  outline: 'none',
  transition: 'border-color 0.2s ease, box-shadow 0.2s ease',
  boxSizing: 'border-box' as const,
};

const fieldErrorBorder: React.CSSProperties = {
  borderColor: '#dc2626',
};

const errorMsgStyle: React.CSSProperties = {
  fontSize: '12px',
  lineHeight: '1.4',
  color: '#dc2626',
  margin: 0,
  minHeight: '0',
};

function useFocusStyles(hasError: boolean) {
  const [focused, setFocused] = React.useState(false);

  const focusRing: React.CSSProperties = focused
    ? hasError
      ? { borderColor: '#dc2626', boxShadow: '0 0 0 3px rgba(220,38,38,0.25)' }
      : { borderColor: '#3b82f6', boxShadow: '0 0 0 3px rgba(59,130,246,0.25)' }
    : {};

  return { focused, setFocused, focusRing };
}

function resolveId(id: string | undefined, name: string | undefined, fallback: string): string {
  return id || name || fallback;
}

/**
 * A styled text input field with label, error state, and focus animation.
 */
export function Input(props: InputProps) {
  const {
    label, name, placeholder, value, onChange, onBlur,
    type = 'text', disabled = false, required = false,
    error, className, id,
  } = props;

  const hasError = Boolean(error);
  const { setFocused, focusRing } = useFocusStyles(hasError);
  const fieldId = resolveId(id, name, `input-${label.replace(/\s+/g, '-').toLowerCase()}`);

  const computedFieldStyle: React.CSSProperties = {
    ...fieldBaseStyle,
    ...(hasError ? fieldErrorBorder : {}),
    ...focusRing,
    ...(disabled ? { backgroundColor: '#f1f5f9', cursor: 'not-allowed' } : {}),
  };

  return (
    <div style={baseWrapperStyle} className={className} data-testid="input-wrapper">
      <label htmlFor={fieldId} style={hasError ? labelErrorStyle : labelStyle}>
        {label}
        {required && <span aria-hidden="true" style={{ color: '#dc2626', marginLeft: 2 }}>*</span>}
      </label>
      <input
        id={fieldId}
        name={name}
        type={type}
        placeholder={placeholder}
        value={value}
        disabled={disabled}
        required={required}
        aria-invalid={hasError}
        aria-describedby={hasError ? `${fieldId}-error` : undefined}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setFocused(true)}
        onBlur={() => { setFocused(false); onBlur?.(); }}
        style={computedFieldStyle}
      />
      {hasError && (
        <p id={`${fieldId}-error`} role="alert" style={errorMsgStyle}>
          {error}
        </p>
      )}
    </div>
  );
}

/**
 * A styled textarea field with label, error state, and focus animation.
 */
export function TextArea(props: TextAreaProps) {
  const {
    label, name, placeholder, value, onChange, onBlur,
    rows = 4, disabled = false, required = false,
    error, className, id,
  } = props;

  const hasError = Boolean(error);
  const { setFocused, focusRing } = useFocusStyles(hasError);
  const fieldId = resolveId(id, name, `textarea-${label.replace(/\s+/g, '-').toLowerCase()}`);

  const computedFieldStyle: React.CSSProperties = {
    ...fieldBaseStyle,
    resize: 'vertical' as const,
    ...(hasError ? fieldErrorBorder : {}),
    ...focusRing,
    ...(disabled ? { backgroundColor: '#f1f5f9', cursor: 'not-allowed' } : {}),
  };

  return (
    <div style={baseWrapperStyle} className={className} data-testid="textarea-wrapper">
      <label htmlFor={fieldId} style={hasError ? labelErrorStyle : labelStyle}>
        {label}
        {required && <span aria-hidden="true" style={{ color: '#dc2626', marginLeft: 2 }}>*</span>}
      </label>
      <textarea
        id={fieldId}
        name={name}
        placeholder={placeholder}
        value={value}
        rows={rows}
        disabled={disabled}
        required={required}
        aria-invalid={hasError}
        aria-describedby={hasError ? `${fieldId}-error` : undefined}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setFocused(true)}
        onBlur={() => { setFocused(false); onBlur?.(); }}
        style={computedFieldStyle}
      />
      {hasError && (
        <p id={`${fieldId}-error`} role="alert" style={errorMsgStyle}>
          {error}
        </p>
      )}
    </div>
  );
}

export default Input;
