FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgtk-3-dev \
    libboost-all-dev \
    libgl1-mesa-glx \
    libopenblas-dev \
    liblapack-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# ✅ Install Python dependencies (including setuptools)
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/ageitgey/face_recognition_models

# Debug check
RUN python -c "import face_recognition_models; print('✅ face_recognition_models installed')"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
