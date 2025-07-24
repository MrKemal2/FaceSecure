FROM python:3.12
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgcc-s1 \
    ffmpeg \
    libsm6 \
    libxext6 \
    cmake \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-backend.txt .

# Upgrade pip and install packages
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements-backend.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]