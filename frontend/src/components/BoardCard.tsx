import React from "react";

/**
 * Represents the board data required by the BoardCard component.
 */
export interface Board {
  /** Display title of the board */
  title: string;
  /** SEO-friendly URL slug */
  slug: string;
  /** Optional longer description of the board */
  description?: string;
  /** Number of columns in the board */
  columnCount: number;
  /** Number of cards across all columns */
  cardCount: number;
}

/**
 * Props for the BoardCard component.
 */
export interface BoardCardProps {
  /** The board data to display */
  board: Board;
}

/**
 * BoardCard – a preview card for the board list page.
 *
 * Displays the board name, description, column/card stats, and links
 * to `/boards/:slug`. Features a modern card design with a gradient
 * accent border on the left side.
 */
const BoardCard: React.FC<BoardCardProps> = ({ board }) => {
  const { title, slug, description, columnCount, cardCount } = board;

  return (
    <a
      href={`/boards/${slug}`}
      data-testid="board-card-link"
      style={{
        display: "block",
        textDecoration: "none",
        color: "inherit",
      }}
    >
      <div
        data-testid="board-card"
        style={{
          position: "relative",
          overflow: "hidden",
          borderRadius: "12px",
          backgroundColor: "#ffffff",
          boxShadow: "0 1px 3px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.04)",
          transition: "box-shadow 0.2s ease, transform 0.2s ease",
          cursor: "pointer",
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.boxShadow =
            "0 4px 12px rgba(0, 0, 0, 0.12), 0 8px 24px rgba(0, 0, 0, 0.08)";
          e.currentTarget.style.transform = "translateY(-2px)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.boxShadow =
            "0 1px 3px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.04)";
          e.currentTarget.style.transform = "translateY(0)";
        }}
      >
        {/* Gradient accent border on the left */}
        <div
          data-testid="board-card-accent"
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            width: "4px",
            height: "100%",
            background: "linear-gradient(180deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%)",
            borderRadius: "12px 0 0 12px",
          }}
        />

        <div style={{ padding: "20px 20px 20px 24px" }}>
          {/* Title */}
          <h3
            data-testid="board-card-title"
            style={{
              margin: "0 0 8px 0",
              fontSize: "18px",
              fontWeight: 600,
              lineHeight: 1.3,
              color: "#1e1b4b",
            }}
          >
            {title}
          </h3>

          {/* Description */}
          {description && (
            <p
              data-testid="board-card-description"
              style={{
                margin: "0 0 16px 0",
                fontSize: "14px",
                lineHeight: 1.5,
                color: "#6b7280",
                display: "-webkit-box",
                WebkitLineClamp: 2,
                WebkitBoxOrient: "vertical",
                overflow: "hidden",
              }}
            >
              {description}
            </p>
          )}

          {/* Stats */}
          <div
            data-testid="board-card-stats"
            style={{
              display: "flex",
              gap: "16px",
              marginTop: description ? "0" : "12px",
            }}
          >
            <span
              data-testid="board-card-column-count"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "6px",
                fontSize: "13px",
                fontWeight: 500,
                color: "#6366f1",
                backgroundColor: "#eef2ff",
                padding: "4px 10px",
                borderRadius: "6px",
              }}
            >
              <svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <rect x="3" y="3" width="7" height="18" rx="1" />
                <rect x="14" y="3" width="7" height="18" rx="1" />
              </svg>
              {columnCount} {columnCount === 1 ? "column" : "columns"}
            </span>

            <span
              data-testid="board-card-card-count"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "6px",
                fontSize: "13px",
                fontWeight: 500,
                color: "#8b5cf6",
                backgroundColor: "#f5f3ff",
                padding: "4px 10px",
                borderRadius: "6px",
              }}
            >
              <svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <rect x="3" y="3" width="18" height="18" rx="2" />
                <line x1="9" y1="3" x2="9" y2="21" />
              </svg>
              {cardCount} {cardCount === 1 ? "card" : "cards"}
            </span>
          </div>
        </div>
      </div>
    </a>
  );
};

export default BoardCard;
