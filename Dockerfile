FROM python:3.12-slim

WORKDIR /app

COPY public/ public/
COPY server.py .

EXPOSE 8000

CMD ["python", "server.py"]
