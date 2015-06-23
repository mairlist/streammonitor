FROM node:0.10

MAINTAINER Torben Weibert <tw@mairlist.com>

RUN npm -g install coffee-script
RUN apt-get update && apt-get -y install curl lame

WORKDIR /app

ADD app /app

RUN npm install

EXPOSE 8000

CMD ["coffee", "app.coffee"]
