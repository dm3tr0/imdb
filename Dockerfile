FROM python:3.9-alpine3.16
COPY . .
EXPOSE 8000
RUN pip install -r requirements.txt
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev\
    && sudo apt-get install gcc

CMD uwsgi --module=project.wsgi:application \
    --master \
    --socket=0.0.0.0:8000 \
    --processes=5 \ 
    --harakiri=20 \
    --max-requests=5000 \
    --vacuum 