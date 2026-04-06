# Real Estate Website — Architecture Document

## Project Overview

A modern real estate listing website built with React, TypeScript, Vite, and Tailwind CSS.

## Project Structure

```
src/
├── types/
│   └── models.ts              # TypeScript interfaces & type aliases
├── data/
│   ├── mockProperties.ts      # 12+ mock property listings
│   ├── mockAgents.ts          # 3+ mock real estate agents
│   └── mockNeighborhoods.ts   # 6 mock neighborhoods
├── components/
│   ├── atoms/                 # Buttons, badges, inputs, icons
│   ├── molecules/             # Cards, forms, nav items
│   └── organisms/             # Header, footer, property grid, hero
├── pages/
│   ├── HomePage.tsx
│   ├── PropertiesPage.tsx
│   ├── PropertyDetailPage.tsx
│   ├── AgentsPage.tsx
│   ├── AgentDetailPage.tsx
│   ├── NeighborhoodsPage.tsx
│   ├── NeighborhoodDetailPage.tsx
│   └── ContactPage.tsx
├── hooks/                     # Custom React hooks
├── utils/                     # Formatting helpers (price, address)
├── App.tsx                    # Root component with React Router
├── main.tsx                   # Entry point
└── index.css                  # Tailwind directives & custom styles
```

## Data Models

All domain models live in `src/types/models.ts`:

| Model            | Purpose                                       |
| ---------------- | --------------------------------------------- |
| `Property`       | A real estate listing with images, price, etc. |
| `Agent`          | A real estate agent / broker                   |
| `Neighborhood`   | A geographic area with aggregate stats         |
| `ContactFormData`| Shape of the contact form submission           |

Supporting union types: `PropertyType`, `PropertyStatus`, `PreferredContact`.

## Routing (React Router v6)

| Path                          | Page                     |
| ----------------------------- | ------------------------ |
| `/`                           | HomePage                 |
| `/properties`                 | PropertiesPage           |
| `/properties/:slug`           | PropertyDetailPage       |
| `/agents`                     | AgentsPage               |
| `/agents/:id`                 | AgentDetailPage          |
| `/neighborhoods`              | NeighborhoodsPage        |
| `/neighborhoods/:slug`        | NeighborhoodDetailPage   |
| `/contact`                    | ContactPage              |

## Mock Data Strategy

- All images use real **Unsplash** photo IDs with the format:
  `https://images.unsplash.com/photo-{ID}?w={W}&h={H}&fit=crop`
- Properties: exterior & interior photography
- Agents: professional headshot portraits
- Neighborhoods: aerial / cityscape / street-level imagery

## Styling

- **Tailwind CSS** utility-first approach
- Design tokens defined via `tailwind.config.js` `extend` section
- Colour palette: slate (neutrals), blue (primary), amber (accent)
- Typography: Inter (sans), Georgia fallback (serif headings)
- Responsive breakpoints: `sm` 640px, `md` 768px, `lg` 1024px, `xl` 1280px

## Build Tooling

| Tool        | Purpose                |
| ----------- | ---------------------- |
| Vite        | Dev server & bundler   |
| TypeScript  | Static type checking   |
| ESLint      | Linting                |
| Prettier    | Code formatting        |
| Vitest      | Unit / integration tests |
