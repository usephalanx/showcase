# Running the Vite React App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 18+ and npm
- Docker (optional, for containerised runs)

## Local Development

```bash
# Install dependencies
npm install

# Start the development server
npm run dev

# Build for production
npm run build

# Preview the production build
npm run preview

# Run tests
npm test
```

## Docker-based Setup

```bash
# Build the Docker image
docker build -t vite-react-app .

# Run the development server
docker run -it --rm -p 5173:5173 vite-react-app npm run dev -- --host

# Run tests inside the container
docker run -it --rm vite-react-app npm test
```

### Dockerfile (example)

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
```

## Project Structure

```
.
├── index.html          # HTML entry point for Vite
├── package.json        # Dependencies and scripts
├── vite.config.js      # Vite configuration with React plugin
├── RUNNING.md          # This file
└── src/
    ├── main.jsx        # React entry point
    ├── App.jsx         # Main App component
    └── App.test.jsx    # Tests for App component
```
