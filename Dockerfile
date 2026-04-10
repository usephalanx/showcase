# Dockerfile for the Hello World React + Vite application.
#
# Uses node:18-alpine as the base image for a lightweight container.
# Installs dependencies and exposes port 5173 for the Vite dev server.

FROM node:18-alpine AS base

WORKDIR /app

# Copy dependency manifests first for better Docker layer caching
COPY package.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application source
COPY . .

# Expose the Vite dev server port
EXPOSE 5173

# Start the Vite development server
CMD ["npm", "run", "dev"]
