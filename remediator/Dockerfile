FROM python:3.9-slim

# Install kubectl inside the container for our simple demo's remediation command
RUN apt-get update && apt-get install -y curl \
    && curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x kubectl && mv kubectl /usr/local/bin/

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY app.py /app/

EXPOSE 8080
CMD ["python", "app.py"]
