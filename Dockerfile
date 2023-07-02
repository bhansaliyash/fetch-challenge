FROM python:3.10-slim

EXPOSE 8000
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /fetch_receipt_processor
COPY . /fetch_receipt_processor

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]