FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install gcc --yes

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory (excluding items in .dockerignore)
COPY . /app

CMD ["python", "-m", "src.app"]
