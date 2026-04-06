import React from "react";

/**
 * Props for the BoardCard component.
 */
export interface BoardCardProps {
  /** Human-readable board title */
  title: string;
  /** URL-friendly slug used for routing */
  slug: string;
  /** Optional board description */
  description?: string | null;
  /** Number of columns in the board */
  columnCount: number;
  /** Total number of cards across all columns */
  cardCount: number;
  /** Optional click handler — when provided, overrides default link behaviour */
  onClick?: (slug: string) => void;
}

/**
 * BoardCard renders a clickable preview card for a Kanban board.
 *
 * Displays the board's title, description (truncated), column count,
 * and card count. Links to `/boards/:slug` by default.
 */
const BoardCard: React.FC<BoardCardProps> = ({
  title,
  slug,
  description,
  columnCount,
  cardCount,
  onClick,
}) => {
  const href = `/boards/${slug}`;

  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    if (onClick) {
      e.preventDefault();
      onClick(slug);
    }
  };

  return (
    <a
      href={href}
      onClick={handleClick}
      data-testid="board-card"
      style={{
        display: "block",
        textDecoration: "none",
        color: "inherit",
        border: "1px solid #e2e8f0",
        borderRadius: "12px",
        padding: "24px",
        backgroundColor: "#ffffff",
        transition: "box-shadow 0.2s ease, transform 0.2s ease",
        cursor: "pointer",
      }}
      onMouseEnter={(e) => {
        const el = e.currentTarget;
        el.style.boxShadow = "0 8px 24px rgba(0, 0, 0, 0.12)";
        el.style.transform = "translateY(-2px)";
      }}
      onMouseLeave={(e) => {
        const el = e.currentTarget;
        el.style.boxShadow = "none";
        el.style.transform = "translateY(0)";
      }}
    >
      <h3
        data-testid="board-card-title"
        style={{
          margin: "0 0 8px 0",
          fontSize: "1.25rem",
          fontWeight: 600,
          lineHeight: 1.3,
          color: "#1a202c",
        }}
      >
        {title}
      </h3>

      {description && (
        <p
          data-testid="board-card-description"
          style={{
            margin: "0 0 16px 0",
            fontSize: "0.875rem",
            lineHeight: 1.5,
            color: "#718096",
            overflow: "hidden",
            display: "-webkit-box",
            WebkitLineClamp: 2,
            WebkitBoxOrient: "vertical",
          }}
        >
          {description}
        </p>
      )}

      <div
        style={{
          display: "flex",
          gap: "16px",
          marginTop: description ? "0" : "16px",
        }}
      >
        <span
          data-testid="board-card-column-count"
          style={{
            fontSize: "0.8125rem",
            color: "#a0aec0",
            fontWeight: 500,
          }}
        >
          {columnCount} {columnCount === 1 ? "column" : "columns"}
        </span>
        <span
          style={{
            fontSize: "0.8125rem",
            color: "#e2e8f0",
          }}
          aria-hidden="true"
        >
          •
        </span>
        <span
          data-testid="board-card-card-count"
          style={{
            fontSize: "0.8125rem",
            color: "#a0aec0",
            fontWeight: 500,
          }}
        >
          {cardCount} {cardCount === 1 ? "card" : "cards"}
        </span>
      </div>
    </a>
  );
};

export default BoardCard;
