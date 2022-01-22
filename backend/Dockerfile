FROM python:3.6-buster

RUN sed -i 's/archive.ubuntu.com/ftp.daumkakao.com/g' /etc/apt/sources.list
RUN apt-get update && apt-get -y install \
        nginx \
        libpq-dev \
        supervisor && \
    apt-get clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/log/nginx/app
RUN mkdir -p /var/log/uwsgi/app
RUN mkdir -p /var/log/supervisor

RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY flask/requirements.txt /var/www/flask/requirements.txt
WORKDIR /var/www/flask
RUN pip3 install -r requirements.txt

EXPOSE 80
EXPOSE 443

CMD ["/usr/bin/supervisord"]
