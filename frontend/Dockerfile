FROM node:6-alpine

RUN apk --no-cache add --virtual .builds-deps build-base python2

COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh

RUN mkdir -p /frontend
WORKDIR /frontend

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
