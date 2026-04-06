import React from "react";
import { useDroppable } from "@dnd-kit/core";
import {
  SortableContext,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";

/**
 * Represents a single card within a column.
 */
export interface ColumnCard {
  id: number;
  title: string;
  slug: string;
  description?: string | null;
  position: number;
  priority?: string | null;
  due_date?: string | null;
}

/**
 * Represents a Kanban column with its cards.
 */
export interface ColumnData {
  id: number;
  title: string;
  position: number;
  color?: string;
  cards: ColumnCard[];
}

export interface BoardColumnProps {
  /** The column data including nested cards. */
  column: ColumnData;
  /** Callback when a card is clicked. Receives the card object. */
  onCardClick?: (card: ColumnCard) => void;
  /** Callback when the "Add card" button is clicked. Receives the column id. */
  onAddCard?: (columnId: number) => void;
  /** Optional render function to render each card. If not provided, a default card is rendered. */
  renderCard?: (card: ColumnCard) => React.ReactNode;
}

/**
 * BoardColumn – A droppable Kanban column that displays a header with title
 * and card count, an accent bar, and a vertical list of cards.
 *
 * Integrates with @dnd-kit as a droppable container and uses SortableContext
 * for sortable children.
 */
const BoardColumn: React.FC<BoardColumnProps> = ({
  column,
  onCardClick,
  onAddCard,
  renderCard,
}) => {
  const accentColor = column.color ?? "#6366f1";

  const { setNodeRef, isOver } = useDroppable({
    id: `column-${column.id}`,
    data: {
      type: "column",
      columnId: column.id,
    },
  });

  const sortableIds = column.cards.map((card) => `card-${card.id}`);

  return (
    <div
      data-testid={`board-column-${column.id}`}
      style={{
        display: "flex",
        flexDirection: "column",
        width: 300,
        minHeight: 200,
        backgroundColor: isOver ? "#f0f0ff" : "#f7f8fa",
        borderRadius: 10,
        overflow: "hidden",
        transition: "background-color 0.2s ease",
      }}
    >
      {/* Accent bar */}
      <div
        data-testid={`column-accent-${column.id}`}
        style={{
          height: 4,
          backgroundColor: accentColor,
          borderTopLeftRadius: 10,
          borderTopRightRadius: 10,
        }}
      />

      {/* Header */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "12px 14px 8px 14px",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <h3
            data-testid={`column-title-${column.id}`}
            style={{
              margin: 0,
              fontSize: 15,
              fontWeight: 600,
              color: "#1e293b",
            }}
          >
            {column.title}
          </h3>
          <span
            data-testid={`column-count-${column.id}`}
            style={{
              fontSize: 12,
              fontWeight: 500,
              color: "#94a3b8",
              backgroundColor: "#e2e8f0",
              borderRadius: 10,
              padding: "2px 8px",
            }}
          >
            {column.cards.length}
          </span>
        </div>

        {onAddCard && (
          <button
            data-testid={`column-add-btn-${column.id}`}
            type="button"
            onClick={() => onAddCard(column.id)}
            aria-label={`Add card to ${column.title}`}
            style={{
              border: "none",
              background: "transparent",
              cursor: "pointer",
              fontSize: 20,
              lineHeight: 1,
              color: "#94a3b8",
              padding: "0 4px",
            }}
          >
            +
          </button>
        )}
      </div>

      {/* Droppable card list */}
      <div
        ref={setNodeRef}
        data-testid={`column-droppable-${column.id}`}
        style={{
          flex: 1,
          padding: "4px 10px 10px 10px",
          display: "flex",
          flexDirection: "column",
          gap: 8,
          minHeight: 60,
        }}
      >
        <SortableContext
          items={sortableIds}
          strategy={verticalListSortingStrategy}
        >
          {column.cards.map((card) =>
            renderCard ? (
              <React.Fragment key={card.id}>
                {renderCard(card)}
              </React.Fragment>
            ) : (
              <div
                key={card.id}
                data-testid={`card-${card.id}`}
                role="button"
                tabIndex={0}
                onClick={() => onCardClick?.(card)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    onCardClick?.(card);
                  }
                }}
                style={{
                  backgroundColor: "#ffffff",
                  borderRadius: 8,
                  padding: "10px 12px",
                  boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
                  cursor: onCardClick ? "pointer" : "default",
                  fontSize: 14,
                  color: "#334155",
                }}
              >
                {card.title}
              </div>
            )
          )}
        </SortableContext>

        {column.cards.length === 0 && (
          <div
            data-testid={`column-empty-${column.id}`}
            style={{
              textAlign: "center",
              color: "#cbd5e1",
              fontSize: 13,
              padding: "16px 0",
            }}
          >
            No cards
          </div>
        )}
      </div>
    </div>
  );
};

export default BoardColumn;
