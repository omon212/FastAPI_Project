# Python 3.11 versiyasidan foydalanamiz
FROM python:3.11

# Ishchi katalogni yaratamiz
WORKDIR /app

# Kerakli kutubxonalarni o'rnatamiz
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini nusxalaymiz
COPY . .

# Alembic migratsiyalarini bajarish va FastAPI'ni ishga tushirish
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
