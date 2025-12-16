FROM python:3.11-slim

# Evita archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiamos dependencias
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código
COPY backend ./backend
COPY templates ./templates

WORKDIR /app/backend

EXPOSE 5000

CMD ["python", "app.py"]
