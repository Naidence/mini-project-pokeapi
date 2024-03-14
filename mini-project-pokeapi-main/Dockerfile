FROM python:3.10-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8080

ENV FLASK_APP=file.py

CMD ["python", "file.py"]
