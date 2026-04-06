import React from "react";

/**
 * Props for the EmptyState component.
 *
 * @property icon - A React node rendered as an illustration-style icon (e.g. an SVG or emoji).
 * @property title - The primary heading text describing the empty state.
 * @property description - A secondary explanatory message.
 * @property actionLabel - Optional label for the call-to-action button.
 * @property onAction - Optional callback invoked when the action button is clicked.
 */
export interface EmptyStateProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
}

/**
 * EmptyState – a centered placeholder UI for when there is no content
 * to display (e.g. no boards, cards, or tags).
 *
 * Renders an illustration-style icon, a title, a description, and an
 * optional call-to-action button.
 */
const EmptyState: React.FC<EmptyStateProps> = ({
  icon,
  title,
  description,
  actionLabel,
  onAction,
}) => {
  return (
    <div
      data-testid="empty-state"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        textAlign: "center",
        padding: "3rem 1.5rem",
        maxWidth: "28rem",
        margin: "0 auto",
      }}
    >
      <div
        data-testid="empty-state-icon"
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          width: "5rem",
          height: "5rem",
          borderRadius: "50%",
          backgroundColor: "#f3f4f6",
          marginBottom: "1.5rem",
          fontSize: "2rem",
          color: "#9ca3af",
        }}
      >
        {icon}
      </div>

      <h3
        data-testid="empty-state-title"
        style={{
          margin: "0 0 0.5rem 0",
          fontSize: "1.25rem",
          fontWeight: 600,
          color: "#111827",
          lineHeight: 1.4,
        }}
      >
        {title}
      </h3>

      <p
        data-testid="empty-state-description"
        style={{
          margin: "0 0 1.5rem 0",
          fontSize: "0.9375rem",
          color: "#6b7280",
          lineHeight: 1.6,
        }}
      >
        {description}
      </p>

      {actionLabel && onAction && (
        <button
          data-testid="empty-state-action"
          type="button"
          onClick={onAction}
          style={{
            display: "inline-flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "0.625rem 1.25rem",
            fontSize: "0.875rem",
            fontWeight: 500,
            color: "#ffffff",
            backgroundColor: "#3b82f6",
            border: "none",
            borderRadius: "0.5rem",
            cursor: "pointer",
            lineHeight: 1,
            transition: "background-color 150ms ease",
          }}
          onMouseEnter={(e) => {
            (e.currentTarget as HTMLButtonElement).style.backgroundColor =
              "#2563eb";
          }}
          onMouseLeave={(e) => {
            (e.currentTarget as HTMLButtonElement).style.backgroundColor =
              "#3b82f6";
          }}
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
};

export default EmptyState;
