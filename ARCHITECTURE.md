# Real Estate Website — Architecture Document

## Overview

A modern real estate listing website built with React, Vite, TypeScript, and Tailwind CSS. The application displays property listings, agent profiles, and neighborhood information with a responsive, professional design.

## Tech Stack

| Layer          | Technology                        |
| -------------- | --------------------------------- |
| Framework      | React 18                          |
| Build Tool     | Vite 5                            |
| Language       | TypeScript 5 (strict mode)        |
| Styling        | Tailwind CSS 4 (via @tailwindcss/vite) |
| Routing        | React Router v6                   |
| Icons          | Lucide React                      |
| Images         | Unsplash source URLs (mock data)  |

## Project Structure

```
├── ARCHITECTURE.md
├── SETUP.md
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.app.json
├── vite.config.ts
├── src/
│   ├── main.tsx                  # Application entry point
│   ├── App.tsx                   # Root component with router
│   ├── index.css                 # Tailwind CSS imports & global styles
│   ├── vite-env.d.ts             # Vite client type declarations
│   ├── types/
│   │   └── models.ts             # TypeScript interfaces & type aliases
│   ├── data/
│   │   ├── mockProperties.ts     # Mock property listings
│   │   ├── mockAgents.ts         # Mock agent profiles
│   │   └── mockNeighborhoods.ts  # Mock neighborhood data
│   ├── components/
│   │   ├── atoms/                # Small, reusable UI primitives
│   │   ├── molecules/            # Composite components
│   │   └── layout/               # Header, Footer, Layout wrappers
│   └── pages/                    # Route-level page components
│       ├── HomePage.tsx
│       ├── PropertiesPage.tsx
│       ├── PropertyDetailPage.tsx
│       ├── AgentsPage.tsx
│       ├── NeighborhoodsPage.tsx
│       └── ContactPage.tsx
└── tests/
    └── *.test.ts
```

## Component Hierarchy

### Atoms
- **Button** — Reusable button with variant props
- **Badge** — Status/tag badge (e.g., "For Sale", "Pending")
- **PriceTag** — Formatted currency display
- **Input** — Styled form input

### Molecules
- **PropertyCard** — Thumbnail card for property listings
- **AgentCard** — Agent profile summary card
- **NeighborhoodCard** — Neighborhood overview card
- **SearchBar** — Property search/filter bar
- **ContactForm** — Contact inquiry form
- **ImageGallery** — Property image carousel/gallery

### Layout
- **Header** — Top navigation bar with logo and links
- **Footer** — Site footer with links and info
- **Layout** — Wraps Header + main content + Footer

### Pages
- **HomePage** — Hero section, featured properties, neighborhoods
- **PropertiesPage** — Full listings grid with filters
- **PropertyDetailPage** — Single property with gallery, details, agent info
- **AgentsPage** — Team/agent directory
- **NeighborhoodsPage** — Neighborhood guide
- **ContactPage** — Contact form and office info

## Routing Structure (React Router v6)

| Path                       | Component            |
| -------------------------- | -------------------- |
| `/`                        | HomePage             |
| `/properties`              | PropertiesPage       |
| `/properties/:slug`        | PropertyDetailPage   |
| `/agents`                  | AgentsPage           |
| `/neighborhoods`           | NeighborhoodsPage    |
| `/contact`                 | ContactPage          |

## Data Models

All TypeScript interfaces are defined in `src/types/models.ts`:

- **Property** — Full property listing with address, specs, images, agent reference
- **Agent** — Real estate agent profile
- **Neighborhood** — Area/neighborhood information
- **ContactFormData** — Contact form submission payload
- **PropertyType** — Union type: `'house' | 'condo' | 'townhouse' | 'apartment' | 'land'`
- **PropertyStatus** — Union type: `'for-sale' | 'pending' | 'sold'`
- **PreferredContact** — Union type: `'email' | 'phone' | 'either'`

## Mock Data Strategy

During development, all data comes from static mock arrays in `src/data/`. Property and agent images use specific Unsplash photo URLs with `w`, `h`, and `fit=crop` query parameters for consistent sizing.

Helper functions are exported alongside the data arrays for common lookups (by slug, by status, by ID, featured items).

## Styling Approach

- **Tailwind CSS 4** via the `@tailwindcss/vite` plugin (no PostCSS config needed)
- Utility-first classes applied directly in JSX
- Design tokens:
  - Primary color: blue-600 / blue-700
  - Accent color: amber-500
  - Neutral palette: slate-50 through slate-900
  - Border radius: rounded-lg (cards), rounded-xl (hero elements)
  - Shadows: shadow-md (cards), shadow-lg (modals/overlays)

## Build Tooling

- **Vite 5** — Fast HMR, optimized production builds
- **TypeScript 5** — Strict mode enabled in tsconfig
- **ESLint** — Linting (configured separately)
- **Prettier** — Code formatting (configured separately)
