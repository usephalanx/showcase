/**
 * Badge/Tag component for displaying category and taxonomy labels.
 *
 * Renders a pill-shaped badge with a subtle background color and darker text.
 * Color can be explicitly provided or auto-generated from the label string via hashing.
 */
import React from "react";

export interface BadgeProps {
  /** The text label to display inside the badge. */
  label: string;
  /**
   * Explicit hex color for the badge (e.g. "#4f46e5").
   * If omitted, a color is deterministically generated from the label string.
   */
  color?: string;
  /** Size variant of the badge. Defaults to "md". */
  size?: "sm" | "md";
  /** Whether to show a remove/close button. Defaults to false. */
  removable?: boolean;
  /** Callback invoked when the remove button is clicked. */
  onRemove?: () => void;
  /** Optional additional CSS class names. */
  className?: string;
}

/**
 * Generate a deterministic HSL-based hex color from an arbitrary string.
 *
 * Uses a simple DJB2-style hash to derive a hue value, then returns
 * a color with fixed saturation (65%) and lightness (45%) to ensure
 * readability as text on a lighter tinted background.
 */
function hashStringToColor(str: string): string {
  let hash = 5381;
  for (let i = 0; i < str.length; i++) {
    hash = (hash * 33) ^ str.charCodeAt(i);
  }
  const hue = Math.abs(hash) % 360;
  return hslToHex(hue, 65, 45);
}

/**
 * Convert HSL values to a hex colour string.
 */
function hslToHex(h: number, s: number, l: number): string {
  const sNorm = s / 100;
  const lNorm = l / 100;
  const a = sNorm * Math.min(lNorm, 1 - lNorm);
  const f = (n: number) => {
    const k = (n + h / 30) % 12;
    const color = lNorm - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
    return Math.round(255 * color)
      .toString(16)
      .padStart(2, "0");
  };
  return `#${f(0)}${f(8)}${f(4)}`;
}

/**
 * Parse a hex color string into its RGB components.
 */
function hexToRgb(hex: string): { r: number; g: number; b: number } {
  const clean = hex.replace(/^#/, "");
  const num = parseInt(clean, 16);
  return {
    r: (num >> 16) & 255,
    g: (num >> 8) & 255,
    b: num & 255,
  };
}

const Badge: React.FC<BadgeProps> = ({
  label,
  color,
  size = "md",
  removable = false,
  onRemove,
  className = "",
}) => {
  const resolvedColor = color ?? hashStringToColor(label);
  const { r, g, b } = hexToRgb(resolvedColor);

  const bgColor = `rgba(${r}, ${g}, ${b}, 0.15)`;
  const textColor = resolvedColor;
  const borderColor = `rgba(${r}, ${g}, ${b}, 0.3)`;

  const sizeStyles: React.CSSProperties =
    size === "sm"
      ? { fontSize: "0.7rem", padding: "0.125rem 0.5rem", lineHeight: "1.4" }
      : { fontSize: "0.8rem", padding: "0.2rem 0.65rem", lineHeight: "1.5" };

  const baseStyles: React.CSSProperties = {
    display: "inline-flex",
    alignItems: "center",
    gap: "0.35rem",
    borderRadius: "9999px",
    fontWeight: 600,
    whiteSpace: "nowrap",
    backgroundColor: bgColor,
    color: textColor,
    border: `1px solid ${borderColor}`,
    maxWidth: "100%",
    ...sizeStyles,
  };

  const buttonStyles: React.CSSProperties = {
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    background: "none",
    border: "none",
    color: textColor,
    cursor: "pointer",
    padding: 0,
    lineHeight: 1,
    fontSize: size === "sm" ? "0.75rem" : "0.9rem",
    opacity: 0.7,
  };

  return (
    <span
      data-testid="badge"
      className={className}
      style={baseStyles}
    >
      <span
        data-testid="badge-label"
        style={{ overflow: "hidden", textOverflow: "ellipsis" }}
      >
        {label}
      </span>
      {removable && (
        <button
          data-testid="badge-remove"
          type="button"
          style={buttonStyles}
          onClick={onRemove}
          aria-label={`Remove ${label}`}
        >
          ×
        </button>
      )}
    </span>
  );
};

export default Badge;
