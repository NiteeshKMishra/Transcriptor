FROM python:3.11-slim-bookworm

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./secrets.env /app/secrets.env
COPY ./web.py /app/web.py
COPY ./app /app/app
COPY ./static /app/static
COPY ./templates /app/templates

EXPOSE 8080

CMD [ "python", "web.py" ]
