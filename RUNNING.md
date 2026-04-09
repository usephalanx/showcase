# Running the Application

## Prerequisites

- **Node.js** 18+ and **npm** 9+ (or use the Docker approach below)

## Local Development

```bash
cd frontend
npm install
npm run dev
```

The dev server starts at [http://localhost:5173](http://localhost:5173).

## Production Build

```bash
cd frontend
npm install
npm run build
npm run preview
```

The preview server starts at [http://localhost:4173](http://localhost:4173).

## Docker

```bash
# Build the image
docker build -t hello-world-app -f frontend/Dockerfile frontend/

# Run the container
docker run -p 8080:80 hello-world-app
```

Open [http://localhost:8080](http://localhost:8080) in your browser.

> **Note:** A `Dockerfile` is not yet included — the commands above
> assume a standard multi-stage Node + nginx setup that can be added
> in a subsequent task.
