# Frontend Setup

## Prerequisites

- Node.js 18+ and npm 9+

## Installation

```bash
cd frontend
npm install
```

## Development

Start the Vite dev server (with API proxy to backend at localhost:8000):

```bash
npm run dev
```

The frontend will be available at http://localhost:5173.

## Running Tests

```bash
npm run test
```

Or in watch mode:

```bash
npm run test:watch
```

## Production Build

```bash
npm run build
npm run preview
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `VITE_API_BASE_URL` | `''` (empty, uses Vite proxy) | Base URL for API requests in production |

Create a `.env` file in the `frontend/` directory for local overrides:

```
VITE_API_BASE_URL=http://localhost:8000
```

## Project Structure

```
frontend/
├── index.html              # HTML entry point
├── package.json            # Dependencies and scripts
├── postcss.config.js       # PostCSS with Tailwind and autoprefixer
├── tailwind.config.js      # Tailwind CSS configuration
├── vite.config.js          # Vite build and dev server config
├── public/
│   └── vite.svg
└── src/
    ├── main.jsx            # React DOM render entry point
    ├── App.jsx             # Root component with route definitions
    ├── index.css           # Tailwind base, components, utilities
    ├── api/                # API client modules
    │   ├── client.js       # Axios instance with JWT interceptor
    │   ├── auth.js         # Auth API calls
    │   ├── projects.js     # Projects API calls
    │   └── tasks.js        # Tasks API calls
    ├── components/         # Reusable UI components
    │   ├── Layout.jsx      # Main layout with nav bar
    │   ├── LoginForm.jsx   # Login form component
    │   └── ProtectedRoute.jsx  # Auth gate wrapper
    ├── context/            # React context providers
    │   └── AuthContext.jsx # JWT auth state management
    ├── hooks/              # Custom React hooks
    │   ├── useAuth.js      # Hook for AuthContext
    │   ├── useProjects.js  # Hook for fetching projects
    │   └── useTasks.js     # Hook for fetching tasks
    ├── pages/              # Page-level components
    │   ├── LoginPage.jsx
    │   ├── ProjectsPage.jsx
    │   └── ProjectDetailPage.jsx
    └── test/               # Test files
        ├── setup.js
        ├── AuthContext.test.jsx
        ├── Layout.test.jsx
        ├── LoginPage.test.jsx
        └── ProtectedRoute.test.jsx
```
