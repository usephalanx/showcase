/**
 * KanbanCard — A single draggable card on a Kanban board.
 *
 * Displays the card title, a truncated description, and tag badges.
 * Wrapped in a react-beautiful-dnd Draggable for drag-and-drop support.
 */

import React from "react";
import { Draggable } from "react-beautiful-dnd";

/** A tag/label that can be attached to a card. */
export interface Tag {
  id: number;
  name: string;
  color?: string;
}

/** The Card data model. */
export interface Card {
  id: number;
  title: string;
  description?: string;
  slug: string;
  tags: Tag[];
}

/** Props accepted by KanbanCard. */
export interface KanbanCardProps {
  /** The card data to display. */
  card: Card;
  /** The index of this card within its column (required by Draggable). */
  index: number;
  /** Maximum characters for the truncated description. Defaults to 120. */
  descriptionMaxLength?: number;
  /** Optional click handler when the card is clicked. */
  onClick?: (card: Card) => void;
}

/**
 * Truncate a string to the given max length, appending an ellipsis if needed.
 */
function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  // Find the last space within the limit to avoid cutting mid-word
  const trimmed = text.slice(0, maxLength);
  const lastSpace = trimmed.lastIndexOf(" ");
  const breakpoint = lastSpace > maxLength * 0.6 ? lastSpace : maxLength;
  return trimmed.slice(0, breakpoint).trimEnd() + "…";
}

/** Default colours cycled through when a tag has no explicit colour. */
const DEFAULT_TAG_COLORS = [
  "#6366f1", // indigo
  "#8b5cf6", // violet
  "#ec4899", // pink
  "#f59e0b", // amber
  "#10b981", // emerald
  "#06b6d4", // cyan
];

function resolveTagColor(tag: Tag, index: number): string {
  return tag.color || DEFAULT_TAG_COLORS[index % DEFAULT_TAG_COLORS.length];
}

const KanbanCard: React.FC<KanbanCardProps> = ({
  card,
  index,
  descriptionMaxLength = 120,
  onClick,
}) => {
  const handleClick = () => {
    if (onClick) onClick(card);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if ((e.key === "Enter" || e.key === " ") && onClick) {
      e.preventDefault();
      onClick(card);
    }
  };

  return (
    <Draggable draggableId={card.slug} index={index}>
      {(provided, snapshot) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          data-testid={`kanban-card-${card.slug}`}
          role="button"
          tabIndex={0}
          onClick={handleClick}
          onKeyDown={handleKeyDown}
          style={{
            userSelect: "none",
            padding: "12px 14px",
            marginBottom: 10,
            borderRadius: 8,
            backgroundColor: snapshot.isDragging ? "#f0f4ff" : "#ffffff",
            boxShadow: snapshot.isDragging
              ? "0 8px 24px rgba(0, 0, 0, 0.15)"
              : "0 1px 3px rgba(0, 0, 0, 0.08)",
            border: "1px solid #e5e7eb",
            cursor: "grab",
            transition: "box-shadow 0.2s ease, transform 0.2s ease, background-color 0.2s ease",
            transform: snapshot.isDragging ? "rotate(2deg)" : undefined,
            ...provided.draggableProps.style,
          }}
          onMouseEnter={(e) => {
            if (!snapshot.isDragging) {
              (e.currentTarget as HTMLElement).style.boxShadow =
                "0 4px 12px rgba(0, 0, 0, 0.12)";
              (e.currentTarget as HTMLElement).style.transform = "translateY(-2px)";
            }
          }}
          onMouseLeave={(e) => {
            if (!snapshot.isDragging) {
              (e.currentTarget as HTMLElement).style.boxShadow =
                "0 1px 3px rgba(0, 0, 0, 0.08)";
              (e.currentTarget as HTMLElement).style.transform = "none";
            }
          }}
        >
          <h3
            style={{
              margin: 0,
              fontSize: 14,
              fontWeight: 600,
              lineHeight: 1.4,
              color: "#1f2937",
            }}
            data-testid="kanban-card-title"
          >
            {card.title}
          </h3>

          {card.description && (
            <p
              style={{
                margin: "6px 0 0",
                fontSize: 12,
                lineHeight: 1.5,
                color: "#6b7280",
              }}
              data-testid="kanban-card-description"
              title={card.description}
            >
              {truncate(card.description, descriptionMaxLength)}
            </p>
          )}

          {card.tags.length > 0 && (
            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: 4,
                marginTop: 8,
              }}
              data-testid="kanban-card-tags"
            >
              {card.tags.map((tag, tagIndex) => {
                const bgColor = resolveTagColor(tag, tagIndex);
                return (
                  <span
                    key={tag.id}
                    data-testid={`kanban-card-tag-${tag.id}`}
                    style={{
                      display: "inline-block",
                      padding: "2px 8px",
                      borderRadius: 9999,
                      fontSize: 11,
                      fontWeight: 500,
                      color: "#ffffff",
                      backgroundColor: bgColor,
                      lineHeight: 1.5,
                    }}
                  >
                    {tag.name}
                  </span>
                );
              })}
            </div>
          )}
        </div>
      )}
    </Draggable>
  );
};

export default KanbanCard;
