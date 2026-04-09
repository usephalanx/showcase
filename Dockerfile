FROM node:20-alpine

WORKDIR /app

# Install dependencies first for better layer caching
COPY package.json ./
RUN npm install

# Copy the rest of the application source
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
