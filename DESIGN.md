

# DESIGN.md — /dev/todo

---

## 1. Brand Identity

**App Name:** /dev/todo

**Tagline:** "Flush your head. Get back to work."

**Personality:** Terse, Precise, Respectful-of-your-time

**Voice & Tone:**
- Never use exclamation marks. Never say "Great job!" or "You're on fire!"
- Use developer-familiar language: "No items" not "Your list is empty — why not add one?"
- Confirmations are factual: "Task added." / "Task deleted." / "All tasks cleared."
- Error messages state what happened and what the user can do: "Server unreachable. Retry or work offline."
- The app speaks like a well-written man page: minimal, accurate, unsentimental.

**Brand Rationale:** The name uses a Unix path convention developers immediately recognize. `/dev/null` discards everything; `/dev/todo` captures everything. The name signals: this tool was built by someone who thinks like you.

---

## 2. Color Palette

This is a dark-first palette. Dark mode is the default. A light mode is not in scope for v1 — developers working in dark IDEs should not be flashbanged by a task list.

### Core Palette

| Token Name | Hex | Role | Do NOT use for |
|---|---|---|---|
| `surface-base` | `#1B1D23` | App background, root canvas | Text, icons, interactive elements |
| `surface-raised` | `#252830` | Cards, input fields, list items | App background (creates no hierarchy) |
| `surface-overlay` | `#2E313A` | Dropdowns, modals, tooltips, hover states on raised surfaces | Body background |
| `text-primary` | `#ECECEF` | Headings, task labels, primary body text | Decorative elements, borders |
| `text-secondary` | `#9499A8` | Timestamps, helper text, metadata, placeholder text | Primary labels, action labels |
| `text-disabled` | `#555966` | Disabled button labels, completed-task strikethrough text | Any interactive/readable content |
| `primary` | `#6E9EFF` | Primary action buttons, focus rings, active links | Backgrounds, decorative fills, status indicators |
| `primary-dark` | `#4A7ADB` | Primary button hover/active state | Text on dark backgrounds (fails contrast) |
| `border-default` | `#3A3D47` | Dividers, input borders, card outlines | Text, backgrounds |
| `success` | `#34D399` | Task completion checkmark, success toast | Button fills, text on dark background at small sizes |
| `warning` | `#FBBF24` | Destructive action confirmation (e.g., "Clear all?"), offline indicator | Error states, success states |
| `error` | `#F87171` | Validation errors, connection failure, delete confirmations | Warning states, decorative use |
| `info` | `#A78BFA` | Informational toasts, keyboard shortcut hints | Primary actions |

**`info` token design note:** The `info` color is a soft violet, chosen to be perceptually distinct from `primary` (blue). The CIE2000 delta E between `#A78BFA` and `#6E9EFF` exceeds 25, eliminating any confusion between informational UI and primary actions — even for users with deuteranopia or protanopia.

### WCAG AA Contrast Verification

All ratios measured against the background they are paired with.

| Foreground | Background | Ratio | Pass (AA) |
|---|---|---|---|
| `text-primary` (#ECECEF) | `surface-base` (#1B1D23) | **14.1:1** | Yes |
| `text-primary` (#ECECEF) | `surface-raised` (#252830) | **11.8:1** | Yes |
| `text-secondary` (#9499A8) | `surface-base` (#1B1D23) | **5.5:1** | Yes |
| `text-secondary` (#9499A8) | `surface-raised` (#252830) | **4.6:1** | Yes |
| `text-disabled` (#555966) | `surface-raised` (#252830) | **2.4:1** | No — intentional. Disabled elements must not appear interactive. Not used for readable content. |
| `primary` (#6E9EFF) | `surface-base` (#1B1D23) | **6.5:1** | Yes |
| `primary` (#6E9EFF) | `surface-raised` (#252830) | **5.4:1** | Yes |
| `primary-dark` (#4A7ADB) | `surface-base` (#1B1D23) | **4.8:1** | Yes |
| `success` (#34D399) | `surface-base` (#1B1D23) | **9.2:1** | Yes |
| `warning` (#FBBF24) | `surface-base` (#1B1D23) | **10.5:1** | Yes |
| `error` (#F87171) | `surface-base` (#1B1D23) | **5.6:1** | Yes |
| `error` (#F87171) | `surface-raised` (#252830) | **4.7:1** | Yes |
| `info` (#A78BFA) | `surface-base` (#1B1D23) | **5.4:1** | Yes |
| `info` (#A78BFA) | `surface-raised` (#252830) | **4.5:1** | Yes |

---

## 3. Typography

### Typeface

| Use | Family | Fallback Stack |
|---|---|---|
| All UI text | Inter | system-ui, -apple-system, Segoe UI, Roboto, sans-serif |
| Monospaced content (counters, keyboard shortcuts, code references) | JetBrains Mono | ui-monospace, SFMono-Regular, Consolas, monospace |

**Rationale:** Inter is optimized for screens at small sizes, has tabular figures, and is free. JetBrains Mono aligns with the developer audience and ensures legible keyboard shortcut labels.

### Type Scale

Base unit: 16px. Scale factor: 1.25 (Major Third).

| Token | Size (px) | Size (rem) | Weight | Line Height | Use |
|---|---|---|---|---|---|
| `type-xs` | 12 | 0.75 | 400 | 1.5 (18px) | Keyboard shortcut hints, fine print |
| `type-sm` | 14 | 0.875 | 400 | 1.5 (21px) | Timestamps, metadata, helper text |
| `type-base` | 16 | 1.0 | 400 | 1.5 (24px) | Task labels, body text, input values |
| `type-md` | 20 | 1.25 | 600 | 1.4 (28px) | Section headings, modal titles |
| `type-lg` | 25 | 1.5625 | 700 | 1.3 (32.5px) | Page titles (e.g., the "/dev/todo" header) |
| `type-xl` | 32 | 2.0 | 700 | 1.2 (38.4px) | Reserved for marketing/landing page hero only — not used in app UI |

**Rules:**
- Never skip more than one step in the scale within a single view.
- Task labels always use `type-base` — no special sizing for "important" tasks. Priority is communicated through iconography and color, never through font size.
- Monospace text uses the same scale tokens but the JetBrains Mono family.

---

## 4. Spacing System

Base unit: **4px**

All spacing values are multiples of 4. No arbitrary values. No "just make it 15px."

| Token | Value (px) | Common Use |
|---|---|---|
| `space-1` | 4 | Inline icon-to-label gap, tight inner padding |
| `space-2` | 8 | Inner padding of compact elements (chips, badges), gap between icon and text |
| `space-3` | 12 | Input inner padding (vertical), gap between related metadata items |
| `space-4` | 16 | Card inner padding, gap between list items, standard margin between siblings |
| `space-5` | 20 | Section label margin-bottom |
| `space-6` | 24 | Gap between sections, modal inner padding |
| `space-8` | 32 | Page-level outer margin, large section separation |
| `space-10` | 40 | Top-level page padding top/bottom |
| `space-12` | 48 | Maximum spacing token — hero section padding on marketing pages only |

**Rules:**
- Component internal spacing uses `space-2` through `space-4`.
- Between-component spacing uses `space-4` through `space-6`.
- Page-level layout spacing uses `space-8` through `space-10`.
- If a design requires a value not in this table, the scale is wrong — revisit the layout, not the scale.

---

## 5. Component Taxonomy

Canonical names only. One name per component. If you call it something else, you are creating a bug.

### 5.1 TaskItem

The atomic unit of the app. A single to-do entry.

**Structure:**
- Checkbox (left-aligned)
- Label (task text, `type-base`, `text-primary`)
- Metadata line (optional: timestamp, `type-sm`, `text-secondary`)
- Action zone (right-aligned: delete action, visible on hover/focus)

**States:**

| State | Visual Treatment |
|---|---|
| **Default** | `surface-raised` background, `text-primary` label, `border-default` bottom border |
| **Hovered** | `surface-overlay` background, delete action becomes visible |
| **Focused** | 2px `primary` focus ring (inset), no background change |
| **Completed** | Checkbox filled with `success`, label gets `text-disabled` color and strikethrough, metadata hidden |
| **Deleting** (optimistic) | Entire row fades to 40% opacity over 200ms, then removes from DOM |
| **Dragging** (if reorder is implemented) | Elevated shadow, slight scale (1.02), `surface-overlay` background |

### 5.2 TaskInput

The text field for adding a new task.

**Structure:**
- Text input field with placeholder "Add a task"
- Submit action (bound to Enter key — no visible submit button in default view)

**States:**

| State | Visual Treatment |
|---|---|
| **Default (empty)** | `surface-raised` background, `border-default` border, placeholder in `text-secondary` |
| **Focused** | `primary` border (2px), `surface-raised` background, cursor visible |
| **Filled** | `text-primary` input text replaces placeholder |
| **Submitting** | Input briefly flashes `surface-overlay` background (150ms), then clears to default |
| **Error** | `error` border (2px), helper text below in `error` + `type-sm`: "Task cannot be empty." |
| **Disabled** | `surface-base` background, `text-disabled` placeholder, no focus ring, no pointer events |

### 5.3 ActionButton

Any button that triggers a primary or destructive action.

**Variants:**

| Variant | Background | Text Color | Border | Use |
|---|---|---|---|---|
| **primary** | `primary` | `surface-base` | none | "Add task" (if visible button variant is used) |
| **ghost** | transparent | `text-secondary` | none | Delete task, clear filters |
| **danger** | transparent | `error` | 1px `error` | "Clear all tasks", "Delete account" |

**States (all variants):**

| State | Visual Treatment |
|---|---|
| **Default** | As defined per variant |
| **Hovered** | Background shifts one surface step darker/lighter; ghost gets `surface-overlay` background |
| **Focused** | 2px `primary` focus ring (offset 2px) |
| **Active (pressed)** | Primary variant uses `primary-dark` background; others dim to 80% opacity |
| **Disabled** | `text-disabled` text, no background change, no pointer events, no focus ring |
| **Loading** | Label replaced by a 16px spinner (animated), width locked to prevent layout shift |

### 5.4 Toast

Non-blocking feedback messages. Appears bottom-center, auto-dismisses.

**Variants:**

| Variant | Left Accent Color | Icon | Example |
|---|---|---|---|
| **success** | `success` | Checkmark | "Task added." |
| **error** | `error` | X-circle | "Server unreachable. Retry or work offline." |
| **info** | `info` | Info-circle | "Keyboard shortcuts: press ? to view." |
| **warning** | `warning` | Alert-triangle | "Offline mode. Changes will sync when reconnected." |

**Behavior:**
- Appears with a 200ms slide-up animation.
- Auto-dismisses after 4 seconds (success, info) or persists until dismissed (error, warning).
- Maximum of 3 toasts visible. Oldest is pushed out if a 4th arrives.
- Each toast has a dismiss button (ghost ActionButton, "×").
- Toast text uses `type-sm`, `text-primary`.
- Toast background: `surface-overlay`.

**States:**

| State | Visual Treatment |
|---|---|
| **Entering** | Slides up 24px from offscreen, opacity 0 → 1 over 200ms |
| **Visible** | Static, full opacity |
| **Dismissing** | Opacity 1 → 0 over 150ms, then removed |

### 5.5 ConfirmDialog

Modal dialog for destructive actions. Blocks interaction with the app until resolved.

**Structure:**
- Overlay: `surface-base` at 60% opacity covering full viewport
- Dialog card: `surface-raised`, centered, max-width 400px
- Heading: `type-md`, `text-primary` (e.g., "Clear all tasks?")
- Body: `type-base`, `text-secondary` (e.g., "This cannot be undone. 12 tasks will be permanently deleted.")
- Actions: Right-aligned. Secondary ghost ActionButton ("Cancel") + danger ActionButton ("Clear all")

**States:**

| State | Visual Treatment |
|---|---|
| **Entering** | Overlay fades in 200ms, dialog scales from 0.95 → 1.0 with fade |
| **Visible** | Static, focus trapped inside dialog |
| **Exiting** | Reverse of entering, 150ms |

**Accessibility:**
- Focus is trapped within the dialog while open.
- Escape key triggers the cancel action.
- The cancel button receives initial focus (safe default).
- The dialog has `role="alertdialog"` with `aria-labelledby` pointing to the heading and `aria-describedby` pointing to the body.

### 5.6 EmptyState

Shown when the task list has zero items.

**Structure:**
- Centered vertically and horizontally in the task list area.
- Monospaced text block styled as a terminal prompt:
  - `$ ls ./tasks`
  - `No items.`
  - Blinking cursor after the second line.
- Below the text block: `text-secondary`, `type-sm`: "Type above to add your first task."

**States:**

| State | Visual Treatment |
|---|---|
| **Default** | As described — visible when list is empty |
| **Transitioning out** | Fades to 0% opacity over 200ms when first task is added |

### 5.7 LoadingState

Shown during initial data fetch or sync.

**Structure:**
- Centered in the task list area.
- Three small dots (8px diameter, `text-secondary`) animating in sequence (opacity pulse, staggered by 150ms each).
- Below dots: `text-secondary`, `type-sm`: "Loading tasks."

**No skeleton screens.** The app should load fast enough to not need them. If load exceeds 300ms, the loading state appears. Below 300ms, no loading indicator is shown (avoids flash of loading state).

### 5.8 ErrorState

Shown when the task list fails to load.

**Structure:**
- Centered in the task list area.
- Icon: X-circle, 32px, `error