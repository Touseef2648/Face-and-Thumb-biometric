FROM python:3.8

WORKDIR /app

COPY . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

Expose 5000

CMD ["python", "main.py"]