# Dockerfile for the Hello World React + Vite application.
#
# Uses Node 18 Alpine for a small image footprint.

FROM node:18-alpine

WORKDIR /app

# Copy dependency manifests first for layer caching
COPY package.json ./

# Install dependencies
RUN npm install

# Copy the rest of the source code
COPY . .

# Expose the Vite dev server port
EXPOSE 5173

# Start the dev server
CMD ["npm", "run", "dev"]
