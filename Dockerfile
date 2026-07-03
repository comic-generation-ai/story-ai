FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY proto/ proto/
COPY scripts/ scripts/
COPY src/ src/

# Compile proto stubs inside the image
RUN python scripts/generate_proto.py

ARG GRPC_PORT=50052
ENV GRPC_PORT=${GRPC_PORT}
EXPOSE ${GRPC_PORT}

CMD ["python", "src/server.py"]
