import React, { useEffect, useState, useCallback } from 'react';
import { Helmet } from 'react-helmet-async';
import { useParams, Link } from 'react-router-dom';
import {
  DndContext,
  DragEndEvent,
  DragOverEvent,
  DragStartEvent,
  DragOverlay,
  PointerSensor,
  useSensor,
  useSensors,
  closestCorners,
} from '@dnd-kit/core';
import {
  SortableContext,
  verticalListSortingStrategy,
  useSortable,
  arrayMove,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

/* ------------------------------------------------------------------ */
/*  Types                                                             */
/* ------------------------------------------------------------------ */

interface Card {
  id: number;
  title: string;
  slug: string;
  description: string | null;
  position: number;
  column_id: number;
}

interface ColumnData {
  id: number;
  title: string;
  position: number;
  cards: Card[];
}

interface Board {
  id: number;
  title: string;
  slug: string;
  description: string | null;
  meta_title: string | null;
  meta_description: string | null;
  columns: ColumnData[];
  created_at: string;
  updated_at: string;
}

/* ------------------------------------------------------------------ */
/*  Sortable Card                                                     */
/* ------------------------------------------------------------------ */

const SortableCard: React.FC<{ card: Card }> = ({ card }) => {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id: `card-${card.id}`,
    data: { type: 'card', card },
  });

  const style: React.CSSProperties = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.4 : 1,
    background: '#fff',
    border: '1px solid #e2e8f0',
    borderRadius: '6px',
    padding: '0.75rem',
    marginBottom: '0.5rem',
    cursor: 'grab',
    boxShadow: isDragging ? '0 4px 12px rgba(0,0,0,0.15)' : '0 1px 3px rgba(0,0,0,0.08)',
  };

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners} data-testid={`card-${card.id}`}>
      <p style={{ margin: 0, fontWeight: 500, fontSize: '0.9rem' }}>{card.title}</p>
      {card.description && (
        <p style={{ margin: '0.25rem 0 0', fontSize: '0.8rem', color: '#718096' }}>
          {card.description.length > 80 ? `${card.description.slice(0, 80)}…` : card.description}
        </p>
      )}
    </div>
  );
};

/* ------------------------------------------------------------------ */
/*  Droppable Column                                                  */
/* ------------------------------------------------------------------ */

interface BoardColumnProps {
  column: ColumnData;
  onAddCard: (columnId: number) => void;
}

const BoardColumn: React.FC<BoardColumnProps> = ({ column, onAddCard }) => {
  const cardIds = column.cards.map((c) => `card-${c.id}`);

  const { setNodeRef } = useSortable({
    id: `column-${column.id}`,
    data: { type: 'column', column },
    disabled: true, // columns not draggable in this iteration
  });

  return (
    <div
      ref={setNodeRef}
      style={{
        minWidth: '300px',
        maxWidth: '300px',
        background: '#f7fafc',
        borderRadius: '8px',
        padding: '0.75rem',
        display: 'flex',
        flexDirection: 'column',
        maxHeight: 'calc(100vh - 200px)',
      }}
      data-testid={`column-${column.id}`}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
        <h3 style={{ margin: 0, fontSize: '1rem', fontWeight: 600 }}>{column.title}</h3>
        <span style={{ fontSize: '0.8rem', color: '#a0aec0' }}>{column.cards.length}</span>
      </div>

      <div style={{ flex: 1, overflowY: 'auto', minHeight: '60px' }}>
        <SortableContext items={cardIds} strategy={verticalListSortingStrategy}>
          {column.cards.map((card) => (
            <SortableCard key={card.id} card={card} />
          ))}
        </SortableContext>
      </div>

      <button
        onClick={() => onAddCard(column.id)}
        style={{
          marginTop: '0.5rem',
          padding: '0.5rem',
          background: 'transparent',
          border: '1px dashed #cbd5e0',
          borderRadius: '6px',
          cursor: 'pointer',
          color: '#718096',
          fontSize: '0.85rem',
          width: '100%',
        }}
      >
        + Add Card
      </button>
    </div>
  );
};

/* ------------------------------------------------------------------ */
/*  Modal                                                             */
/* ------------------------------------------------------------------ */

interface ModalProps {
  isOpen: boolean;
  title: string;
  onClose: () => void;
  children: React.ReactNode;
}

const Modal: React.FC<ModalProps> = ({ isOpen, title, onClose, children }) => {
  if (!isOpen) return null;
  return (
    <div
      style={{
        position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.4)',
        display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000,
      }}
      onClick={onClose}
      data-testid="modal-overlay"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: '#fff', borderRadius: '8px', padding: '1.5rem',
          minWidth: '360px', maxWidth: '480px', boxShadow: '0 8px 32px rgba(0,0,0,0.2)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h2 style={{ margin: 0, fontSize: '1.1rem' }}>{title}</h2>
          <button onClick={onClose} style={{ background: 'none', border: 'none', fontSize: '1.2rem', cursor: 'pointer' }}>×</button>
        </div>
        {children}
      </div>
    </div>
  );
};

/* ------------------------------------------------------------------ */
/*  BoardPage                                                         */
/* ------------------------------------------------------------------ */

const BoardPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const [board, setBoard] = useState<Board | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeCard, setActiveCard] = useState<Card | null>(null);

  // Modal state
  const [addColumnOpen, setAddColumnOpen] = useState(false);
  const [addCardColumnId, setAddCardColumnId] = useState<number | null>(null);
  const [newColumnTitle, setNewColumnTitle] = useState('');
  const [newCardTitle, setNewCardTitle] = useState('');
  const [newCardDescription, setNewCardDescription] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 5 } }),
  );

  /* ---- Fetch board ---- */
  const fetchBoard = useCallback(async () => {
    if (!slug) return;
    try {
      setLoading(true);
      const res = await fetch(`/api/boards/${slug}`);
      if (!res.ok) {
        throw new Error(res.status === 404 ? 'Board not found.' : `Failed to load board (HTTP ${res.status})`);
      }
      const data: Board = await res.json();
      // Ensure cards have column_id set
      data.columns.forEach((col) => col.cards.forEach((c) => { c.column_id = col.id; }));
      data.columns.sort((a, b) => a.position - b.position);
      data.columns.forEach((col) => col.cards.sort((a, b) => a.position - b.position));
      setBoard(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  }, [slug]);

  useEffect(() => { void fetchBoard(); }, [fetchBoard]);

  /* ---- Helpers ---- */
  const findColumnByCardId = (cardDndId: string): ColumnData | undefined => {
    if (!board) return undefined;
    const cardId = parseInt(cardDndId.replace('card-', ''), 10);
    return board.columns.find((col) => col.cards.some((c) => c.id === cardId));
  };

  /* ---- Drag handlers ---- */
  const handleDragStart = (event: DragStartEvent) => {
    const { active } = event;
    const data = active.data.current;
    if (data?.type === 'card') setActiveCard(data.card as Card);
  };

  const handleDragOver = (event: DragOverEvent) => {
    const { active, over } = event;
    if (!over || !board) return;

    const activeId = String(active.id);
    const overId = String(over.id);
    if (activeId === overId) return;

    const sourceCol = findColumnByCardId(activeId);
    let destCol: ColumnData | undefined;

    if (overId.startsWith('card-')) {
      destCol = findColumnByCardId(overId);
    } else if (overId.startsWith('column-')) {
      const colId = parseInt(overId.replace('column-', ''), 10);
      destCol = board.columns.find((c) => c.id === colId);
    }

    if (!sourceCol || !destCol || sourceCol.id === destCol.id) return;

    // Move card across columns optimistically
    setBoard((prev) => {
      if (!prev) return prev;
      const cardId = parseInt(activeId.replace('card-', ''), 10);
      const cardIndex = sourceCol.cards.findIndex((c) => c.id === cardId);
      if (cardIndex === -1) return prev;

      const card = { ...sourceCol.cards[cardIndex], column_id: destCol!.id };
      const newColumns = prev.columns.map((col) => {
        if (col.id === sourceCol.id) {
          return { ...col, cards: col.cards.filter((c) => c.id !== cardId) };
        }
        if (col.id === destCol!.id) {
          const overCardId = overId.startsWith('card-') ? parseInt(overId.replace('card-', ''), 10) : -1;
          const overIndex = col.cards.findIndex((c) => c.id === overCardId);
          const newCards = [...col.cards.filter((c) => c.id !== cardId)];
          if (overIndex >= 0) {
            newCards.splice(overIndex, 0, card);
          } else {
            newCards.push(card);
          }
          return { ...col, cards: newCards };
        }
        return col;
      });
      return { ...prev, columns: newColumns };
    });
  };

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;
    setActiveCard(null);
    if (!over || !board) return;

    const activeId = String(active.id);
    const overId = String(over.id);
    const cardId = parseInt(activeId.replace('card-', ''), 10);

    // Find current column of this card after drag-over
    const col = board.columns.find((c) => c.cards.some((card) => card.id === cardId));
    if (!col) return;

    // Same-column reorder
    if (activeId !== overId && overId.startsWith('card-')) {
      const oldIndex = col.cards.findIndex((c) => `card-${c.id}` === activeId);
      const newIndex = col.cards.findIndex((c) => `card-${c.id}` === overId);
      if (oldIndex !== -1 && newIndex !== -1 && oldIndex !== newIndex) {
        setBoard((prev) => {
          if (!prev) return prev;
          return {
            ...prev,
            columns: prev.columns.map((c) =>
              c.id === col.id ? { ...c, cards: arrayMove(c.cards, oldIndex, newIndex) } : c,
            ),
          };
        });
      }
    }

    // Calculate new position
    const cardIndex = col.cards.findIndex((c) => c.id === cardId);
    const newPosition = cardIndex >= 0 ? cardIndex : col.cards.length;

    // Persist via API
    try {
      await fetch(`/api/cards/${cardId}/move`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ column_id: col.id, position: newPosition }),
      });
    } catch {
      // Revert on failure
      void fetchBoard();
    }
  };

  /* ---- Add Column ---- */
  const handleAddColumn = async () => {
    if (!board || !newColumnTitle.trim()) return;
    setSubmitting(true);
    try {
      const res = await fetch(`/api/boards/${board.id}/columns`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newColumnTitle.trim(), position: board.columns.length }),
      });
      if (res.ok) {
        setNewColumnTitle('');
        setAddColumnOpen(false);
        void fetchBoard();
      }
    } finally {
      setSubmitting(false);
    }
  };

  /* ---- Add Card ---- */
  const handleAddCard = async () => {
    if (addCardColumnId === null || !newCardTitle.trim()) return;
    const col = board?.columns.find((c) => c.id === addCardColumnId);
    setSubmitting(true);
    try {
      const res = await fetch(`/api/columns/${addCardColumnId}/cards`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: newCardTitle.trim(),
          description: newCardDescription.trim() || null,
          position: col ? col.cards.length : 0,
        }),
      });
      if (res.ok) {
        setNewCardTitle('');
        setNewCardDescription('');
        setAddCardColumnId(null);
        void fetchBoard();
      }
    } finally {
      setSubmitting(false);
    }
  };

  /* ---- SEO ---- */
  const pageTitle = board?.meta_title ?? (board ? `${board.title} — Kanban Board` : 'Board — Kanban Board');
  const pageDescription = board?.meta_description ?? board?.description ?? 'View and manage your Kanban board columns and cards.';
  const canonicalUrl = slug ? `${window.location.origin}/boards/${slug}` : undefined;

  /* ---- Render ---- */
  return (
    <>
      <Helmet>
        <title>{pageTitle}</title>
        <meta name="description" content={pageDescription} />
        <meta property="og:title" content={pageTitle} />
        <meta property="og:description" content={pageDescription} />
        <meta property="og:type" content="website" />
        {canonicalUrl && <link rel="canonical" href={canonicalUrl} />}
        {canonicalUrl && <meta property="og:url" content={canonicalUrl} />}
        {board && (
          <script type="application/ld+json">
            {JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'WebPage',
              name: board.title,
              description: board.description ?? '',
              url: canonicalUrl,
            })}
          </script>
        )}
      </Helmet>

      <div style={{ padding: '1.5rem', minHeight: '100vh', background: '#edf2f7' }}>
        {loading && (
          <p role="status" style={{ textAlign: 'center', padding: '2rem', color: '#718096' }}>
            Loading board…
          </p>
        )}

        {error && (
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <p role="alert" style={{ color: '#e53e3e', marginBottom: '1rem' }}>{error}</p>
            <Link to="/" style={{ color: '#3182ce', textDecoration: 'none' }}>← Back to all boards</Link>
          </div>
        )}

        {!loading && !error && board && (
          <>
            {/* Header */}
            <div style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
              <Link to="/" style={{ color: '#3182ce', textDecoration: 'none', fontWeight: 500 }}>← Boards</Link>
              <h1 style={{ fontSize: '1.5rem', margin: 0 }}>{board.title}</h1>
            </div>

            {board.description && (
              <p style={{ color: '#718096', marginBottom: '1.5rem', maxWidth: '600px' }}>{board.description}</p>
            )}

            {/* Kanban columns */}
            <DndContext
              sensors={sensors}
              collisionDetection={closestCorners}
              onDragStart={handleDragStart}
              onDragOver={handleDragOver}
              onDragEnd={handleDragEnd}
            >
              <div
                style={{
                  display: 'flex',
                  gap: '1rem',
                  overflowX: 'auto',
                  paddingBottom: '1rem',
                  alignItems: 'flex-start',
                }}
                data-testid="board-columns"
              >
                {board.columns.length === 0 && (
                  <div style={{ textAlign: 'center', padding: '3rem', color: '#a0aec0', width: '100%' }}>
                    <p style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>No columns yet.</p>
                    <p>Create your first column to get started!</p>
                  </div>
                )}

                {board.columns.map((col) => (
                  <BoardColumn
                    key={col.id}
                    column={col}
                    onAddCard={(colId) => {
                      setAddCardColumnId(colId);
                      setNewCardTitle('');
                      setNewCardDescription('');
                    }}
                  />
                ))}

                {/* Add column button */}
                <button
                  onClick={() => { setAddColumnOpen(true); setNewColumnTitle(''); }}
                  style={{
                    minWidth: '280px',
                    padding: '1rem',
                    background: 'rgba(255,255,255,0.6)',
                    border: '2px dashed #cbd5e0',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    color: '#718096',
                    fontSize: '0.95rem',
                    fontWeight: 500,
                    flexShrink: 0,
                  }}
                  data-testid="add-column-btn"
                >
                  + Add Column
                </button>
              </div>

              <DragOverlay>
                {activeCard ? (
                  <div
                    style={{
                      background: '#fff',
                      border: '1px solid #e2e8f0',
                      borderRadius: '6px',
                      padding: '0.75rem',
                      boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
                      width: '280px',
                    }}
                  >
                    <p style={{ margin: 0, fontWeight: 500 }}>{activeCard.title}</p>
                  </div>
                ) : null}
              </DragOverlay>
            </DndContext>
          </>
        )}
      </div>

      {/* Add Column Modal */}
      <Modal isOpen={addColumnOpen} title="Add Column" onClose={() => setAddColumnOpen(false)}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <input
            type="text"
            placeholder="Column title"
            value={newColumnTitle}
            onChange={(e) => setNewColumnTitle(e.target.value)}
            autoFocus
            style={{ padding: '0.5rem 0.75rem', border: '1px solid #e2e8f0', borderRadius: '6px', fontSize: '0.95rem' }}
            data-testid="column-title-input"
            onKeyDown={(e) => { if (e.key === 'Enter') void handleAddColumn(); }}
          />
          <button
            onClick={() => void handleAddColumn()}
            disabled={submitting || !newColumnTitle.trim()}
            style={{
              padding: '0.5rem 1rem',
              background: '#3182ce',
              color: '#fff',
              border: 'none',
              borderRadius: '6px',
              cursor: submitting ? 'not-allowed' : 'pointer',
              fontWeight: 500,
              opacity: submitting || !newColumnTitle.trim() ? 0.6 : 1,
            }}
          >
            {submitting ? 'Creating…' : 'Create Column'}
          </button>
        </div>
      </Modal>

      {/* Add Card Modal */}
      <Modal
        isOpen={addCardColumnId !== null}
        title="Add Card"
        onClose={() => setAddCardColumnId(null)}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <input
            type="text"
            placeholder="Card title"
            value={newCardTitle}
            onChange={(e) => setNewCardTitle(e.target.value)}
            autoFocus
            style={{ padding: '0.5rem 0.75rem', border: '1px solid #e2e8f0', borderRadius: '6px', fontSize: '0.95rem' }}
            data-testid="card-title-input"
            onKeyDown={(e) => { if (e.key === 'Enter') void handleAddCard(); }}
          />
          <textarea
            placeholder="Description (optional)"
            value={newCardDescription}
            onChange={(e) => setNewCardDescription(e.target.value)}
            rows={3}
            style={{ padding: '0.5rem 0.75rem', border: '1px solid #e2e8f0', borderRadius: '6px', fontSize: '0.95rem', resize: 'vertical' }}
            data-testid="card-description-input"
          />
          <button
            onClick={() => void handleAddCard()}
            disabled={submitting || !newCardTitle.trim()}
            style={{
              padding: '0.5rem 1rem',
              background: '#3182ce',
              color: '#fff',
              border: 'none',
              borderRadius: '6px',
              cursor: submitting ? 'not-allowed' : 'pointer',
              fontWeight: 500,
              opacity: submitting || !newCardTitle.trim() ? 0.6 : 1,
            }}
          >
            {submitting ? 'Creating…' : 'Create Card'}
          </button>
        </div>
      </Modal>
    </>
  );
};

export default BoardPage;
