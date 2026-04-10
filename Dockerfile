FROM node:18-alpine AS base

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

# Run tests
FROM base AS test
RUN npm test

# Development server
FROM base AS dev
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
