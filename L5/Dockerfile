FROM python:3.9-slim

RUN apt-get update && apt-get install -y libfreetype6-dev libpng-dev && apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["/bin/bash"]
