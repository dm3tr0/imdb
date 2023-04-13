FROM python:3.9

ADD requirements.txt /requirements.txt
RUN apt update; apt install -y gettext; rm -rf /var/apt/cache; apt install gcc
RUN pip install -r /requirements.txt


ADD . /src
WORKDIR /src


CMD uwsgi --module "django.core.wsgi:get_wsgi_application()" \
    --master --pidfile=/tmp/project-master.pid \
    --http=0.0.0.0:8000 \
    --processes=4 \
    --harakiri=20 \
    --max-requests=5000 \
    --vacuum \
    --enable-threads
