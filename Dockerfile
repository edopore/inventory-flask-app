FROM python:bookworm

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.tx

CMD ["python3","api.py"]

