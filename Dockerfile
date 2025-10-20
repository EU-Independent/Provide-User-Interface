FROM python:3.9-slim
 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
 
WORKDIR /app
 
COPY requirements.txt /app/
 
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    procps \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
 
COPY . /app/
 
EXPOSE 8000
 
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
