FROM python:3.11-bullseye

# Install dependencies
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    python3-gdal \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
# GDAL requires these environment variables to be set

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

#Copy and install requirements

WORKDIR /app
COPY requirements.txt .

#Cartopy often requires Cython to be installed first

RUN pip install --no-cache-dir cython
RUN pip install --no-cache-dir -r requirements.txt
COPY data/ ./data/
COPY Maps/ ./Maps/ 
COPY scripts/ ./scripts/
CMD ["python", "scripts/location_map.py"]
