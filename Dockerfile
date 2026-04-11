FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY app/ /code/app/
COPY main.py /code/main.py
COPY routes.py /code/routes.py
COPY models.py /code/models.py
COPY storage.py /code/storage.py
COPY conftest.py /code/conftest.py

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
