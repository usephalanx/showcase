# Real Estate Website — Architecture Document

## Overview

A modern, responsive real estate website built with React, TypeScript, Vite, and Tailwind CSS. The application showcases property listings, agent profiles, and neighborhood information with a contact system.

## Tech Stack

| Layer         | Technology                       |
| ------------- | -------------------------------- |
| Framework     | React 18+                        |
| Language      | TypeScript 5+                    |
| Build Tool    | Vite 5+                          |
| Routing       | React Router v6 (BrowserRouter)  |
| Styling       | Tailwind CSS 4+                  |
| Linting       | ESLint, Prettier                 |
| Data          | Mock data (static JSON-like TS)  |
| Images        | Unsplash source URLs             |

## Project Structure

```
├── index.html                  # HTML entry point
├── ARCHITECTURE.md             # This file
├── package.json
├── tsconfig.json
├── vite.config.ts
├── src/
│   ├── main.tsx                # React DOM render + BrowserRouter
│   ├── App.tsx                 # Route definitions
│   ├── index.css               # Tailwind directives
│   ├── types/
│   │   └── models.ts           # TypeScript interfaces & type aliases
│   ├── data/
│   │   ├── mockProperties.ts   # Mock property listings
│   │   ├── mockAgents.ts       # Mock agent profiles
│   │   └── mockNeighborhoods.ts# Mock neighborhood data
│   ├── pages/
│   │   ├── HomePage.tsx        # Landing page with featured listings
│   │   ├── PropertyDetailPage.tsx # Single property view
│   │   └── ContactPage.tsx     # Contact form
│   └── components/             # Reusable UI components (future phases)
│       ├── atoms/              # Buttons, inputs, badges
│       ├── molecules/          # Cards, list items, form groups
│       └── organisms/          # Header, footer, property grid
└── tests/
    ├── models.test.ts          # Type/data validation tests
    ├── mockData.test.ts        # Mock data helper tests
    └── App.test.tsx            # Route rendering tests
```

## Routing

| Path              | Component            | Description                     |
| ----------------- | -------------------- | ------------------------------- |
| `/`               | `HomePage`           | Featured listings & hero        |
| `/property/:id`   | `PropertyDetailPage` | Single property detail view     |
| `/contact`        | `ContactPage`        | Contact form                    |

## Data Models

### Property

Represents a real estate listing with full details including location, features, pricing, associated agent, and neighborhood.

### Agent

Represents a real estate agent with contact info, bio, specialties, and social links.

### Neighborhood

Represents a neighborhood area with walkability scores, average prices, and highlights.

### ContactFormData

Captures user-submitted contact/inquiry form data.

## Mock Data Strategy

All data is served from static TypeScript modules in `src/data/`. Images use stable Unsplash photo URLs with explicit width/height/fit parameters to ensure consistent rendering. Helper functions provide filtered and lookup access to the data.

## Design Tokens (Tailwind)

- **Primary**: Slate-based neutral palette (`slate-50` through `slate-900`)
- **Accent**: Blue (`blue-600`, `blue-700`) for CTAs and links
- **Success**: Green (`green-600`) for status indicators
- **Warning**: Amber (`amber-500`) for pending states
- **Font**: System font stack via Tailwind defaults
- **Spacing**: Tailwind's default 4px-based scale
- **Breakpoints**: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px)
