/**
 * Reusable Modal dialog component built on @headlessui/react Dialog.
 *
 * Features:
 * - Backdrop blur with fade animation
 * - Slide-in + scale content animation
 * - Close on Escape key and backdrop click (handled by Headless UI)
 * - Accessible focus trap (handled by Headless UI)
 * - Three size variants: sm, md, lg
 * - Clean modern styling with rounded corners and subtle shadow
 */

import React, { Fragment } from "react";
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  Transition,
  TransitionChild,
} from "@headlessui/react";

export interface ModalProps {
  /** Whether the modal is currently open. */
  isOpen: boolean;
  /** Callback invoked when the modal should close. */
  onClose: () => void;
  /** Title displayed in the modal header. */
  title: string;
  /** Content rendered inside the modal body. */
  children: React.ReactNode;
  /** Width variant of the modal. Defaults to "md". */
  size?: "sm" | "md" | "lg";
}

const sizeClasses: Record<NonNullable<ModalProps["size"]>, string> = {
  sm: "sm:max-w-sm",
  md: "sm:max-w-md",
  lg: "sm:max-w-lg",
};

export default function Modal({
  isOpen,
  onClose,
  title,
  children,
  size = "md",
}: ModalProps): React.JSX.Element {
  return (
    <Transition show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        {/* Backdrop */}
        <TransitionChild
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div
            className="fixed inset-0 bg-black/40 backdrop-blur-sm"
            aria-hidden="true"
            data-testid="modal-backdrop"
          />
        </TransitionChild>

        {/* Full-screen container for centering */}
        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4">
            {/* Panel */}
            <TransitionChild
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              enterTo="opacity-100 translate-y-0 sm:scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 translate-y-0 sm:scale-100"
              leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            >
              <DialogPanel
                className={`w-full ${sizeClasses[size]} transform rounded-xl bg-white p-6 shadow-xl transition-all`}
                data-testid="modal-panel"
              >
                {/* Header */}
                <div className="flex items-center justify-between mb-4">
                  <DialogTitle
                    as="h2"
                    className="text-lg font-semibold leading-6 text-gray-900"
                    data-testid="modal-title"
                  >
                    {title}
                  </DialogTitle>
                  <button
                    type="button"
                    className="rounded-md p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"
                    onClick={onClose}
                    aria-label="Close"
                    data-testid="modal-close-button"
                  >
                    <svg
                      className="h-5 w-5"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      strokeWidth={1.5}
                      stroke="currentColor"
                      aria-hidden="true"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>

                {/* Body */}
                <div data-testid="modal-body">{children}</div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}
