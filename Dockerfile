# Multi-stage Dockerfile for the Mini React Counter application.

# Stage 1: Install dependencies and build
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve with a lightweight static server
FROM node:20-alpine AS production
WORKDIR /app
RUN npm install -g serve@14
COPY --from=build /app/dist ./dist
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
