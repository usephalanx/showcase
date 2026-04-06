# Setup Instructions

## Frontend

### Prerequisites
- Node.js >= 18
- npm >= 9

### Install Dependencies

```bash
cd frontend
npm install
```

### Run Development Server

```bash
cd frontend
npm run dev
```

### Run Tests

```bash
cd frontend
npm test
```

### Build for Production

```bash
cd frontend
npm run build
```

## Backend

### Prerequisites
- Python >= 3.11
- pip

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Run Development Server

```bash
cd backend
uvicorn app.main:app --reload
```

### Run Tests

```bash
cd backend
python -m pytest
```

## Notes

- Do NOT commit generated lock files (package-lock.json, poetry.lock, etc.) — generate them locally via the install commands above.
- Do NOT commit node_modules/, __pycache__/, .venv/, dist/, or build/ directories.
