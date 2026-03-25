FROM python:3.14-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache build-base \
  && pip install --no-cache-dir -r requirements.txt \
  && apk del build-base

COPY . .

COPY .env /app/.env
RUN chmod +r /app/.env || true

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "--verbosity=2", "0.0.0.0:8000"]
