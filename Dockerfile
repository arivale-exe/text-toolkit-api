FROM python:3.11-slim

WORKDIR /app

COPY text_toolkit/ ./text_toolkit/
COPY setup.py ./

RUN pip install --no-cache-dir -e .

EXPOSE 8090

HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8090/ || exit 1

CMD ["python3", "-m", "text_toolkit", "--port", "8090"]