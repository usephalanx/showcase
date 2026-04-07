# Maddie Real Estate Landing Page — Architecture Document

## Overview

A single-page luxury real estate landing page built with React, Vite, TypeScript, and Tailwind CSS. The page showcases a real estate agent's brand, recent sales, and contact information with a warm, elegant aesthetic.

---

## File & Folder Structure

```
/
├── index.html                  # Root HTML with Google Fonts & meta tags
├── package.json                # Dependencies and scripts
├── vite.config.js              # Vite config with React plugin & path aliases
├── tailwind.config.js          # Tailwind design tokens
├── postcss.config.js           # PostCSS plugins (tailwindcss, autoprefixer)
├── tsconfig.json               # TypeScript compiler options
├── tsconfig.node.json          # TypeScript config for Node (Vite config)
├── ARCHITECTURE.md             # This file
├── SETUP.md                    # Setup instructions
├── src/
│   ├── main.tsx                # React entry point
│   ├── App.tsx                 # Root application component
│   ├── index.css               # Global styles & Tailwind directives
│   ├── vite-env.d.ts           # Vite client type declarations
│   ├── components/
│   │   ├── Header.tsx          # Fixed navigation bar
│   │   ├── Hero.tsx            # Full-width hero section
│   │   ├── About.tsx           # About / agent profile section
│   │   ├── RecentSales.tsx     # Property cards grid
│   │   ├── PropertyCard.tsx    # Individual property card
│   │   ├── Contact.tsx         # Contact form / CTA section
│   │   ├── Footer.tsx          # Site footer
│   │   └── ScrollToTop.tsx     # Scroll-to-top utility button
│   ├── hooks/
│   │   └── useSmoothScroll.ts  # Hook for smooth scroll-to-id navigation
│   ├── utils/
│   │   └── scrollTo.ts         # Utility function for smooth scrolling
│   └── types/
│       └── index.ts            # Shared TypeScript interfaces
└── tests/
    └── test_config.py          # Validation tests for config files
```

---

## Component Tree

```
App
├── Header
│   └── Nav links (smooth scroll anchors)
├── Hero
│   └── CTA Button
├── About
│   └── Profile image + bio text
├── RecentSales
│   └── PropertyCard[] (grid of 3–6 cards)
├── Contact
│   └── Contact form / CTA
├── Footer
│   └── Social links, copyright
└── ScrollToTop
```

---

## Design Tokens

### Color Palette

| Token             | Hex       | Usage                                |
|-------------------|-----------|--------------------------------------|
| cream             | `#FDF8F0` | Primary background                   |
| cream-light       | `#FFFDF7` | Card backgrounds, subtle contrast    |
| cream-dark        | `#F5EDE0` | Borders, dividers                    |
| slate-900         | `#1E293B` | Primary headings                     |
| slate-700         | `#334155` | Body text                            |
| slate-500         | `#64748B` | Secondary text                       |
| slate-400         | `#94A3B8` | Muted text, placeholders             |
| gold              | `#C9A84C` | Primary accent                       |
| gold-light        | `#D4B968` | Hover states                         |
| gold-lighter      | `#E8D5A3` | Subtle accent backgrounds            |
| gold-dark         | `#B8943F` | Active states                        |
| warm-white        | `#FAF7F2` | Alternate section background         |

### Typography

| Element        | Font Family       | Weights          | Sizes (desktop)       |
|----------------|-------------------|------------------|-----------------------|
| h1             | Playfair Display  | 700              | 4xl–6xl               |
| h2             | Playfair Display  | 600, 700         | 3xl–4xl               |
| h3             | Playfair Display  | 500, 600         | 2xl–3xl               |
| h4–h6          | Playfair Display  | 500              | xl–2xl                |
| body           | Inter             | 300, 400, 500    | base–lg               |
| button         | Inter             | 500, 600         | sm–base               |
| caption        | Inter             | 400              | sm                    |

Fonts are loaded via Google Fonts CDN in `index.html`.

### Responsive Breakpoints

| Breakpoint | Min Width | Usage                          |
|------------|-----------|--------------------------------|
| sm         | 640px     | Mobile landscape               |
| md         | 768px     | Tablet portrait                |
| lg         | 1024px    | Tablet landscape / small laptop|
| xl         | 1280px    | Desktop                        |
| 2xl        | 1536px    | Large desktop                  |

These are Tailwind defaults — no overrides needed.

---

## Section Order

1. **Header / Nav** — Fixed top bar with logo and smooth-scroll nav links
2. **Hero** — Full-viewport hero with background image, heading, and CTA
3. **About / Profile** — Agent photo + bio with split layout
4. **Recent Sales** — Grid of property cards with images, price, details
5. **Contact** — Contact form or CTA block
6. **Footer** — Branding, social links, legal

---

## Image Strategy

Curated Unsplash images (free to use):

- **Hero**: `https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1920&q=80` (luxury home exterior)
- **About**: `https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=800&q=80` (professional portrait)
- **Property 1**: `https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600&q=80`
- **Property 2**: `https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=600&q=80`
- **Property 3**: `https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=600&q=80`

---

## Smooth Scroll Implementation

1. `html { scroll-behavior: smooth; }` in `index.html` and `src/index.css`
2. `scrollTo.ts` utility: `document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })`
3. `useSmoothScroll` hook wraps the utility for use in nav links
4. Each section has an `id` attribute matching the nav link href

---

## Tailwind Customizations

See `tailwind.config.js` for the full configuration. Key extensions:

- **colors**: cream, gold, warm-white palettes added alongside Tailwind slate
- **fontFamily**: `playfair` → `['Playfair Display', 'serif']`, `inter` → `['Inter', 'sans-serif']`
- **spacing**: `18` (4.5rem), `88` (22rem), `128` (32rem) for hero/section sizing
- **maxWidth**: `8xl` (88rem) for wide section containers
- **animation**: `fade-in`, `slide-up` for entrance animations
- **keyframes**: Custom keyframes for the above animations
