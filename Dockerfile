# Dockerfile for Hello World React+Vite application
FROM node:18-alpine

WORKDIR /app

# Copy package manifest first for layer caching
COPY package.json ./

# Install dependencies
RUN npm install

# Copy the rest of the source code
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start the Vite dev server, binding to all interfaces
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
