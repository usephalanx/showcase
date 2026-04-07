# Running the Project

**Maddie — Luxury Real Estate Agent Landing Page built with React + Vite + Tailwind CSS.**

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Node.js** (v18 or later recommended) — [https://nodejs.org/](https://nodejs.org/)
- **npm** (v9 or later, bundled with Node.js)

You can verify your installation by running:

```bash
node --version
npm --version
```

---

## Install Dependencies

From the project root directory, install all required packages:

```bash
npm install
```

This will read `package.json` and install both production dependencies (React, React DOM) and development dependencies (Vite, Tailwind CSS, PostCSS, Autoprefixer, and the Vite React plugin).

---

## Run the Development Server

Start the local development server with hot module replacement (HMR):

```bash
npm run dev
```

Once started, the application will be available at:

```
http://localhost:3000
```

The dev server watches for file changes and automatically reloads the browser. Tailwind CSS classes are processed on the fly via PostCSS.

---

## Build for Production

Create an optimized, minified production build:

```bash
npm run build
```

The output is written to the `dist/` directory. This bundle is ready for deployment to any static hosting provider (Vercel, Netlify, AWS S3, GitHub Pages, etc.).

---

## Preview the Production Build

After building, you can preview the production bundle locally:

```bash
npm run preview
```

This starts a local static file server that serves the contents of `dist/`, allowing you to verify the production build before deploying.

---

## Project Structure Overview

```
.
├── index.html            # Root HTML entry point with Google Fonts
├── package.json          # Project manifest and scripts
├── vite.config.js        # Vite configuration with React plugin
├── tailwind.config.js    # Tailwind CSS design tokens and customizations
├── postcss.config.js     # PostCSS plugin configuration
├── src/
│   ├── main.jsx          # React entry point
│   ├── index.css         # Global styles and Tailwind directives
│   └── ...               # React components and assets
├── dist/                 # Production build output (generated)
└── RUNNING.md            # This file
```

---

## Tech Stack

| Technology      | Purpose                        |
| --------------- | ------------------------------ |
| React           | UI component library           |
| Vite            | Build tool and dev server      |
| Tailwind CSS    | Utility-first CSS framework    |
| PostCSS         | CSS processing pipeline        |
| Autoprefixer    | Vendor prefix management       |
