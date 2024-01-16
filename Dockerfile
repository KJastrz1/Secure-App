
FROM python:3.11.7-slim

WORKDIR /secureApp

COPY . /secureApp

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "secureApp:app"]
