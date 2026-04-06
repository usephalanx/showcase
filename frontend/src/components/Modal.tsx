import React, { useEffect, useCallback, useRef } from "react";

/**
 * Props for the Modal component.
 */
export interface ModalProps {
  /** Whether the modal is currently visible. */
  isOpen: boolean;
  /** Callback invoked when the modal requests to be closed. */
  onClose: () => void;
  /** Title displayed in the modal header. */
  title: string;
  /** Content rendered inside the modal body. */
  children: React.ReactNode;
}

const overlayStyle: React.CSSProperties = {
  position: "fixed",
  inset: 0,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  backgroundColor: "rgba(0, 0, 0, 0.5)",
  zIndex: 1000,
};

const panelStyle: React.CSSProperties = {
  backgroundColor: "#ffffff",
  borderRadius: "8px",
  padding: "24px",
  minWidth: "320px",
  maxWidth: "560px",
  width: "100%",
  boxShadow: "0 4px 24px rgba(0, 0, 0, 0.15)",
  position: "relative",
};

const headerStyle: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  marginBottom: "16px",
};

const titleStyle: React.CSSProperties = {
  margin: 0,
  fontSize: "1.25rem",
  fontWeight: 600,
  lineHeight: 1.4,
};

const closeButtonStyle: React.CSSProperties = {
  background: "none",
  border: "none",
  fontSize: "1.5rem",
  cursor: "pointer",
  lineHeight: 1,
  padding: "4px 8px",
  color: "#666",
};

/**
 * A reusable modal dialog with overlay, centered content panel, and close
 * button.  Closes on overlay click or Escape key press.
 */
const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children }) => {
  const panelRef = useRef<HTMLDivElement>(null);

  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onClose();
      }
    },
    [onClose],
  );

  useEffect(() => {
    if (isOpen) {
      document.addEventListener("keydown", handleKeyDown);
      return () => {
        document.removeEventListener("keydown", handleKeyDown);
      };
    }
  }, [isOpen, handleKeyDown]);

  // Move focus into the panel when opened for accessibility.
  useEffect(() => {
    if (isOpen && panelRef.current) {
      panelRef.current.focus();
    }
  }, [isOpen]);

  if (!isOpen) {
    return null;
  }

  const handleOverlayClick = (event: React.MouseEvent<HTMLDivElement>) => {
    // Only close when the overlay itself (not the panel) is clicked.
    if (event.target === event.currentTarget) {
      onClose();
    }
  };

  return (
    <div
      style={overlayStyle}
      data-testid="modal-overlay"
      onClick={handleOverlayClick}
      role="presentation"
    >
      <div
        ref={panelRef}
        role="dialog"
        aria-modal="true"
        aria-label={title}
        tabIndex={-1}
        style={panelStyle}
        data-testid="modal-panel"
      >
        <div style={headerStyle}>
          <h2 style={titleStyle} data-testid="modal-title">
            {title}
          </h2>
          <button
            type="button"
            onClick={onClose}
            style={closeButtonStyle}
            aria-label="Close modal"
            data-testid="modal-close-button"
          >
            ×
          </button>
        </div>
        <div data-testid="modal-body">{children}</div>
      </div>
    </div>
  );
};

export default Modal;
