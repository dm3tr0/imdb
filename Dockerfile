FROM python:3.9-alpine3.16
COPY . .
EXPOSE 8000
RUN pip install -r requirements.txt
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
