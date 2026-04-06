/**
 * KanbanCard – A draggable card component for Kanban boards.
 *
 * Displays a card's title, truncated description, and category badges.
 * Features subtle shadow, hover lift effect, and grab cursor for drag.
 * Links to /cards/:slug for SEO-friendly navigation.
 */

import React from "react";
import Badge from "./Badge";

/** Represents a category associated with a card. */
export interface CardCategory {
  id: number;
  name: string;
  slug: string;
}

/** Represents the card data structure matching the backend Card model. */
export interface Card {
  id: number;
  title: string;
  slug: string;
  description?: string | null;
  position: number;
  column_id: number;
  categories: CardCategory[];
}

export interface KanbanCardProps {
  /** The card data to render. */
  card: Card;
  /** Callback invoked when the card is clicked. */
  onClick?: (card: Card) => void;
  /** Maximum number of characters before description is truncated. */
  maxDescriptionLength?: number;
}

/**
 * Truncates a string to the given max length, appending an ellipsis
 * if the original exceeds that length.
 */
function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) {
    return text;
  }
  const truncated = text.slice(0, maxLength).trimEnd();
  return `${truncated}…`;
}

const KanbanCard: React.FC<KanbanCardProps> = ({
  card,
  onClick,
  maxDescriptionLength = 120,
}) => {
  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    if (onClick) {
      e.preventDefault();
      onClick(card);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLAnchorElement>) => {
    if (e.key === "Enter" || e.key === " ") {
      if (onClick) {
        e.preventDefault();
        onClick(card);
      }
    }
  };

  const description =
    card.description && card.description.trim().length > 0
      ? truncateText(card.description.trim(), maxDescriptionLength)
      : null;

  return (
    <a
      href={`/cards/${card.slug}`}
      data-testid="kanban-card"
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      style={{
        display: "block",
        textDecoration: "none",
        color: "inherit",
        backgroundColor: "#ffffff",
        borderRadius: "8px",
        padding: "12px 14px",
        boxShadow: "0 1px 3px rgba(0, 0, 0, 0.1)",
        cursor: "grab",
        transition: "transform 0.15s ease, box-shadow 0.15s ease",
        border: "1px solid #e5e7eb",
      }}
      onMouseEnter={(e) => {
        const el = e.currentTarget;
        el.style.transform = "translateY(-2px)";
        el.style.boxShadow = "0 4px 12px rgba(0, 0, 0, 0.15)";
      }}
      onMouseLeave={(e) => {
        const el = e.currentTarget;
        el.style.transform = "translateY(0)";
        el.style.boxShadow = "0 1px 3px rgba(0, 0, 0, 0.1)";
      }}
      role="article"
      aria-label={card.title}
    >
      <h3
        data-testid="kanban-card-title"
        style={{
          margin: "0 0 6px 0",
          fontSize: "14px",
          fontWeight: 600,
          lineHeight: 1.3,
          color: "#111827",
        }}
      >
        {card.title}
      </h3>

      {description && (
        <p
          data-testid="kanban-card-description"
          style={{
            margin: "0 0 10px 0",
            fontSize: "12px",
            lineHeight: 1.5,
            color: "#6b7280",
          }}
        >
          {description}
        </p>
      )}

      {card.categories.length > 0 && (
        <div
          data-testid="kanban-card-badges"
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "4px",
            marginTop: description ? "0" : "8px",
          }}
        >
          {card.categories.map((category) => (
            <Badge key={category.id} label={category.name} />
          ))}
        </div>
      )}
    </a>
  );
};

export default KanbanCard;
