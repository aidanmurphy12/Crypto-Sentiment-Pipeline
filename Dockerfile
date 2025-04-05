FROM python:3.11.4-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["jupyter", "notebook", "--notebook-dir=/notebooks", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
