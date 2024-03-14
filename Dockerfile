FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

COPY . /app

EXPOSE 5000

#ENV FLASK_APP=app.py

CMD ["gunicorn", "-b", "0.0.0.0:8080",  "file:app"]
