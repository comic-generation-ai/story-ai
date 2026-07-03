FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

ARG PORT=50052
ENV PORT=${PORT}
EXPOSE ${PORT}

CMD ["python", "src/server.py"]
