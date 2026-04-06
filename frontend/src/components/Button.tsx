import React from "react";

export interface ButtonProps {
  /** Visual style variant */
  variant?: "primary" | "secondary" | "ghost" | "danger";
  /** Size of the button */
  size?: "sm" | "md" | "lg";
  /** Whether the button is disabled */
  disabled?: boolean;
  /** Whether the button is in a loading state */
  loading?: boolean;
  /** Click handler */
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  /** Button content */
  children: React.ReactNode;
  /** Optional HTML button type */
  type?: "button" | "submit" | "reset";
  /** Optional extra className */
  className?: string;
  /** Accessible label when loading */
  loadingText?: string;
}

const variantStyles: Record<string, React.CSSProperties> = {
  primary: {
    backgroundColor: "#2563eb",
    color: "#ffffff",
    border: "1px solid #2563eb",
  },
  secondary: {
    backgroundColor: "#ffffff",
    color: "#1f2937",
    border: "1px solid #d1d5db",
  },
  ghost: {
    backgroundColor: "transparent",
    color: "#1f2937",
    border: "1px solid transparent",
  },
  danger: {
    backgroundColor: "#dc2626",
    color: "#ffffff",
    border: "1px solid #dc2626",
  },
};

const hoverVariantStyles: Record<string, React.CSSProperties> = {
  primary: { backgroundColor: "#1d4ed8" },
  secondary: { backgroundColor: "#f3f4f6" },
  ghost: { backgroundColor: "#f3f4f6" },
  danger: { backgroundColor: "#b91c1c" },
};

const sizeStyles: Record<string, React.CSSProperties> = {
  sm: { padding: "4px 12px", fontSize: "13px", lineHeight: "20px" },
  md: { padding: "8px 16px", fontSize: "14px", lineHeight: "22px" },
  lg: { padding: "12px 24px", fontSize: "16px", lineHeight: "24px" },
};

const baseStyle: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  gap: "8px",
  fontFamily: "inherit",
  fontWeight: 500,
  borderRadius: "6px",
  cursor: "pointer",
  transition: "background-color 150ms ease, box-shadow 150ms ease, opacity 150ms ease",
  outline: "none",
  textDecoration: "none",
  whiteSpace: "nowrap",
  userSelect: "none",
};

const disabledStyle: React.CSSProperties = {
  opacity: 0.5,
  cursor: "not-allowed",
};

const focusRingStyle: React.CSSProperties = {
  boxShadow: "0 0 0 3px rgba(59, 130, 246, 0.5)",
};

const Spinner: React.FC<{ size: string }> = ({ size }) => {
  const dim = size === "sm" ? 14 : size === "lg" ? 20 : 16;
  return (
    <svg
      data-testid="button-spinner"
      width={dim}
      height={dim}
      viewBox="0 0 24 24"
      fill="none"
      style={{ animation: "button-spin 0.75s linear infinite" }}
      aria-hidden="true"
    >
      <circle
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="3"
        strokeLinecap="round"
        strokeDasharray="31.4 31.4"
      />
    </svg>
  );
};

export default function Button({
  variant = "primary",
  size = "md",
  disabled = false,
  loading = false,
  onClick,
  children,
  type = "button",
  className,
  loadingText,
}: ButtonProps) {
  const [hovered, setHovered] = React.useState(false);
  const [focused, setFocused] = React.useState(false);

  const isDisabled = disabled || loading;

  const combinedStyle: React.CSSProperties = {
    ...baseStyle,
    ...sizeStyles[size],
    ...variantStyles[variant],
    ...(hovered && !isDisabled ? hoverVariantStyles[variant] : {}),
    ...(focused && !isDisabled ? focusRingStyle : {}),
    ...(isDisabled ? disabledStyle : {}),
  };

  return (
    <>
      <style>{`@keyframes button-spin { to { transform: rotate(360deg); } }`}</style>
      <button
        type={type}
        style={combinedStyle}
        disabled={isDisabled}
        onClick={onClick}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        className={className}
        aria-disabled={isDisabled}
        aria-busy={loading}
        aria-label={loading && loadingText ? loadingText : undefined}
      >
        {loading && <Spinner size={size} />}
        {children}
      </button>
    </>
  );
}
