FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /uvx /bin/

RUN apt-get update && apt-get -y install \
        nginx \
        supervisor \
        build-essential && \
    apt-get clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/log/nginx/app
RUN mkdir -p /var/log/uwsgi/app
RUN mkdir -p /var/log/supervisor

RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# The venv lives outside /var/www/flask because the dev compose bind-mounts
# the source tree over that path.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV PATH=/opt/venv/bin:$PATH

COPY flask/pyproject.toml flask/uv.lock /var/www/flask/
WORKDIR /var/www/flask
RUN uv sync --frozen --no-dev

EXPOSE 80
EXPOSE 443

CMD ["/usr/bin/supervisord"]
