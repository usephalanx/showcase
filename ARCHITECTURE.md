# Maddie | Luxury Real Estate — Architecture Document

## Overview

A single-page luxury real estate landing page built with React, TypeScript,
Tailwind CSS, and Vite. The design emphasizes elegance through a refined
color palette, premium typography, and smooth interactions.

---

## File & Folder Structure

```
├── index.html
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
├── vite.config.ts
├── ARCHITECTURE.md
├── SETUP.md
├── public/
│   └── vite.svg
├── src/
│   ├── main.tsx              # React entry point
│   ├── App.tsx               # Root component
│   ├── index.css             # Global styles & Tailwind directives
│   ├── components/
│   │   ├── Header.tsx        # Navigation bar
│   │   ├── Hero.tsx          # Hero section with CTA
│   │   ├── About.tsx         # Agent profile / about section
│   │   ├── RecentSales.tsx   # Property cards grid
│   │   ├── PropertyCard.tsx  # Individual property card
│   │   ├── Contact.tsx       # Contact form section
│   │   └── Footer.tsx        # Site footer
│   ├── utils/
│   │   └── scrollTo.ts       # Smooth scroll-to-id utility
│   └── types/
│       └── index.ts          # Shared TypeScript interfaces
└── tests/
    ├── setup.ts              # Test setup (jsdom, jest-dom)
    ├── test_index_html.test.ts
    ├── test_main.test.tsx
    └── test_index_css.test.ts
```

---

## Component Tree

```
App
├── Header (sticky nav, logo, nav links, CTA button)
├── Hero (background image, headline, sub-headline, dual CTAs)
├── About (agent photo, bio, statistics row)
├── RecentSales (section heading, PropertyCard[] grid)
│   └── PropertyCard (image, address, price, beds/baths/sqft)
├── Contact (form: name, email, phone, message, submit)
└── Footer (logo, links, social icons, copyright)
```

---

## Design Tokens

### Color Palette

| Token          | Hex       | Usage                          |
| -------------- | --------- | ------------------------------ |
| cream          | `#FFFDF7` | Page background                |
| cream-dark     | `#FFF8F0` | Card backgrounds, alternation  |
| slate-900      | `#0F172A` | Heading text                   |
| slate-700      | `#334155` | Body text                      |
| slate-500      | `#64748B` | Secondary/muted text           |
| slate-400      | `#94A3B8` | Placeholder, borders           |
| gold           | `#C8A951` | Primary accent, buttons        |
| gold-dark      | `#B8963E` | Hover states                   |
| gold-medium    | `#D4B968` | Gradient mid-point             |
| gold-light     | `#E8D5A3` | Gradient highlight, decorative |

### Gold Gradient

```css
background: linear-gradient(135deg, #C8A951 0%, #E8D5A3 50%, #D4B968 100%);
```

---

## Typography

| Role     | Font Family       | Weights            |
| -------- | ----------------- | ------------------ |
| Headings | Playfair Display  | 400, 500, 600, 700 |
| Body     | Inter             | 300, 400, 500, 600, 700 |

Fonts are loaded via Google Fonts `<link>` in `index.html` with
`preconnect` hints for optimal loading.

---

## Responsive Breakpoints

| Name | Min Width | Usage                      |
| ---- | --------- | -------------------------- |
| sm   | 640px     | Tablet portrait            |
| md   | 768px     | Tablet landscape           |
| lg   | 1024px    | Desktop                    |
| xl   | 1280px    | Large desktop              |

---

## Section Order

1. **Header / Navigation** — Sticky top, glass-morphism effect
2. **Hero** — Full-viewport, background image, gradient overlay
3. **About / Profile** — Two-column layout (image + bio)
4. **Recent Sales** — 3-column responsive grid of property cards
5. **Contact** — Centered form with gold accent border
6. **Footer** — Dark background, multi-column links

---

## Smooth Scroll Implementation

1. CSS `scroll-behavior: smooth` on `<html>` element
2. React utility `scrollTo(id: string)` that calls
   `document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })`
3. Navigation links use `href="#section-id"` with `onClick` calling the
   scroll utility for enhanced control

---

## Curated Image Sources (Unsplash)

- **Hero**: Luxury home exterior — `https://images.unsplash.com/photo-1600596542815-ffad4c1539a9`
- **About**: Professional headshot — `https://images.unsplash.com/photo-1573496359142-b8d87734a5a2`
- **Property 1**: Modern villa — `https://images.unsplash.com/photo-1600585154340-be6161a56a0c`
- **Property 2**: Penthouse — `https://images.unsplash.com/photo-1600607687939-ce8a6c25118c`
- **Property 3**: Estate — `https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea`

---

## Tailwind Customizations

See `tailwind.config.js` for full configuration. Key extensions:

- Custom color tokens (cream, gold variants)
- Font family aliases (`font-playfair`, `font-inter`)
- `max-w-8xl` (88rem) for wide section containers
- Custom spacing values for fine-tuned layouts
