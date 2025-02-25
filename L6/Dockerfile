FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libxcb-xinerama0 \
    libxkbcommon-x11-0 \
    libxcb-cursor0 \
    libegl1 \
    libgl1-mesa-glx \
    libglu1-mesa \
    libqt5gui5 \
    libqt5widgets5 \
    libqt5quick5 \
    libxcb-keysyms1 \
    libxi6 \
    x11-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV DISPLAY=:0

CMD ["/bin/bash"]
