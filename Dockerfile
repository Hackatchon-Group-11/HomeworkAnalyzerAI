# Python 3.10 imajını temel alıyoruz
FROM python:3.10-slim

# Gerekli sistem kütüphanelerini yükleyelim
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    libcairo2 \
    libffi-dev \
    libglib2.0-0 \
    libxml2 \
    libxslt1.1 \
    shared-mime-info \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Proje dosyalarını konteynıra ekleyelim
WORKDIR /app
COPY . /app


# WeasyPrint ve bağımlılıkları yükleyelim
RUN pip install --no-cache-dir --timeout=120 -r requirements.txt
RUN python -m spacy download xx_ent_wiki_sm


# Uygulamayı çalıştırmak için gerekli komut
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]


