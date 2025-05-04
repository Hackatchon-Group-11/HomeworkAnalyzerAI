# Temel imaj: Debian tabanlı bir Python imajı
FROM python:3.10-slim

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    libcairo2 \
    libffi-dev \
    libglib2.0-0 \
    libgobject-2.0-0 \
    libxml2 \
    libxslt1.1 \
    shared-mime-info \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Uygulama dizini
WORKDIR /app

# Gereken dosyaları kopyala
COPY . /app

# Python bağımlılıklarını kur
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Port tanımla
EXPOSE 5000

# Uygulamayı başlat
CMD ["python", "main.py"]
