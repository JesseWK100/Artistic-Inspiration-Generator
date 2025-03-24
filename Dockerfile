FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

# Copy and install requirements
COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY app/ /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
