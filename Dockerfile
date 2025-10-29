# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# system deps for some packages (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY app /app/app

# expose port
EXPOSE 8000

# default command to run (can be overridden by docker-compose)
CMD ["uvicorn", "app.router:app", "--host", "0.0.0.0", "--port", "8000"]
