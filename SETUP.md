# Setup Instructions

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Install Test Dependencies

```bash
pip install pytest httpx
```

## Run Tests

```bash
pytest tests/ -v
```

## Run the Application

```bash
uvicorn main:app --reload
```
