import React, { forwardRef, useId } from "react";

export interface TextAreaProps
  extends Omit<React.TextareaHTMLAttributes<HTMLTextAreaElement>, "onChange"> {
  /** Label text displayed above the textarea */
  label?: string;
  /** Placeholder text shown when the textarea is empty */
  placeholder?: string;
  /** Controlled value */
  value?: string;
  /** Change handler receiving the new string value */
  onChange?: (value: string) => void;
  /** Error message to display; truthy value triggers error styling */
  error?: string;
  /** Helper text displayed below the textarea when there is no error */
  helperText?: string;
  /** Whether the field is required */
  required?: boolean;
  /** Whether the field is disabled */
  disabled?: boolean;
  /** Number of visible text rows */
  rows?: number;
}

const TextArea = forwardRef<HTMLTextAreaElement, TextAreaProps>(
  (
    {
      label,
      placeholder,
      value,
      onChange,
      error,
      helperText,
      required = false,
      disabled = false,
      rows = 4,
      id: externalId,
      className = "",
      ...rest
    },
    ref
  ) => {
    const generatedId = useId();
    const textareaId = externalId || generatedId;
    const hasError = Boolean(error);
    const bottomText = hasError ? error : helperText;

    const baseClasses =
      "block w-full rounded-md border px-3 py-2 text-sm leading-6 transition-all duration-200 outline-none resize-y";
    const normalClasses =
      "border-gray-300 bg-white text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30";
    const errorClasses =
      "border-red-500 bg-white text-gray-900 placeholder-gray-400 focus:border-red-500 focus:ring-2 focus:ring-red-500/30";
    const disabledClasses = "bg-gray-50 text-gray-500 cursor-not-allowed opacity-60";

    const textareaClasses = [
      baseClasses,
      hasError ? errorClasses : normalClasses,
      disabled ? disabledClasses : "",
      className,
    ]
      .filter(Boolean)
      .join(" ");

    return (
      <div className="flex flex-col gap-1">
        {label && (
          <label
            htmlFor={textareaId}
            className="text-sm font-medium text-gray-700"
          >
            {label}
            {required && (
              <span className="ml-0.5 text-red-500" aria-hidden="true">
                *
              </span>
            )}
          </label>
        )}
        <textarea
          ref={ref}
          id={textareaId}
          value={value}
          placeholder={placeholder}
          disabled={disabled}
          required={required}
          rows={rows}
          aria-invalid={hasError}
          aria-describedby={bottomText ? `${textareaId}-description` : undefined}
          onChange={(e) => onChange?.(e.target.value)}
          className={textareaClasses}
          {...rest}
        />
        {bottomText && (
          <p
            id={`${textareaId}-description`}
            className={`text-xs ${
              hasError ? "text-red-600" : "text-gray-500"
            }`}
            role={hasError ? "alert" : undefined}
          >
            {bottomText}
          </p>
        )}
      </div>
    );
  }
);

TextArea.displayName = "TextArea";

export default TextArea;
