# ---------------------------------------------------------------------------
# Dockerfile for the React + Vite development environment
# ---------------------------------------------------------------------------
FROM node:18-alpine AS base

WORKDIR /app

# Copy dependency manifests first for better layer caching
COPY package.json ./

# Install dependencies
RUN npm install

# Copy the rest of the source code
COPY . .

# Expose the Vite dev server port
EXPOSE 5173

# Start the Vite dev server, listening on all interfaces
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
