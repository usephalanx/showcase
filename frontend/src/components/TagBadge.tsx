/**
 * TagBadge component — displays a tag as a pill-shaped badge with its color.
 *
 * Supports two sizes (sm/md), optional remove button, and click handler.
 * Automatically computes text color (black or white) for contrast against
 * the tag's background color.
 */
import React from "react";

export interface TagBadgeProps {
  /** Display name of the tag */
  name: string;
  /** URL-safe slug for the tag */
  slug: string;
  /** CSS hex color string, e.g. "#e74c3c" */
  color: string;
  /** Badge size variant */
  size?: "sm" | "md";
  /** Whether to show the remove (×) button */
  removable?: boolean;
  /** Called when the remove button is clicked; receives the slug */
  onRemove?: (slug: string) => void;
  /** Called when the badge itself is clicked; receives the slug */
  onClick?: (slug: string) => void;
}

/**
 * Compute relative luminance of a hex colour and return "#000" or "#fff"
 * for best contrast.
 *
 * Uses the W3C relative luminance formula:
 *   L = 0.2126 * R + 0.7152 * G + 0.0722 * B
 * where each channel is linearised from sRGB.
 */
function contrastTextColor(hex: string): string {
  const cleaned = hex.replace(/^#/, "");
  const fullHex =
    cleaned.length === 3
      ? cleaned
          .split("")
          .map((c) => c + c)
          .join("")
      : cleaned;

  const r = parseInt(fullHex.substring(0, 2), 16) / 255;
  const g = parseInt(fullHex.substring(2, 4), 16) / 255;
  const b = parseInt(fullHex.substring(4, 6), 16) / 255;

  const linearize = (c: number) =>
    c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);

  const luminance =
    0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b);

  return luminance > 0.179 ? "#000000" : "#ffffff";
}

const TagBadge: React.FC<TagBadgeProps> = ({
  name,
  slug,
  color,
  size = "md",
  removable = false,
  onRemove,
  onClick,
}) => {
  const textColor = contrastTextColor(color);

  const sizeClasses =
    size === "sm"
      ? "text-xs px-2 py-0.5 gap-1"
      : "text-sm px-3 py-1 gap-1.5";

  const handleClick = (e: React.MouseEvent<HTMLSpanElement>) => {
    e.preventDefault();
    if (onClick) {
      onClick(slug);
    }
  };

  const handleRemove = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    e.preventDefault();
    if (onRemove) {
      onRemove(slug);
    }
  };

  const removeIconSize = size === "sm" ? "h-3 w-3" : "h-3.5 w-3.5";

  return (
    <span
      data-testid={`tag-badge-${slug}`}
      role={onClick ? "button" : undefined}
      tabIndex={onClick ? 0 : undefined}
      onClick={onClick ? handleClick : undefined}
      onKeyDown={
        onClick
          ? (e: React.KeyboardEvent<HTMLSpanElement>) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onClick(slug);
              }
            }
          : undefined
      }
      className={`inline-flex items-center rounded-full font-medium leading-none select-none transition-opacity hover:opacity-90 ${sizeClasses} ${
        onClick ? "cursor-pointer" : ""
      }`}
      style={{ backgroundColor: color, color: textColor }}
    >
      <span data-testid="tag-badge-name">{name}</span>
      {removable && (
        <button
          type="button"
          data-testid={`tag-badge-remove-${slug}`}
          aria-label={`Remove tag ${name}`}
          onClick={handleRemove}
          className={`inline-flex items-center justify-center rounded-full hover:bg-black/20 transition-colors ${removeIconSize}`}
          style={{ color: textColor }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 16 16"
            fill="currentColor"
            className={removeIconSize}
            aria-hidden="true"
          >
            <path d="M4.28 3.22a.75.75 0 0 0-1.06 1.06L6.94 8l-3.72 3.72a.75.75 0 1 0 1.06 1.06L8 9.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L9.06 8l3.72-3.72a.75.75 0 0 0-1.06-1.06L8 6.94 4.28 3.22Z" />
          </svg>
        </button>
      )}
    </span>
  );
};

export default TagBadge;
