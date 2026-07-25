# Setup

## Prerequisites

- Python 3.9+

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the application

```bash
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000 in your browser.

## Running tests

```bash
pytest tests/ -v
```
