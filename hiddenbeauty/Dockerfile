FROM nginx:1.19.1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         build-essential \
         imagemagick \
         npm \
         nginx \
         python3 \
         python3-dev \
         python3-pip \
         python3-wheel \
         python3-pil \
         uwsgi \
         uwsgi-plugin-python3 \
         libpcre3-dev \
         libz-dev \
         zip \
    && rm -rf /var/lib/apt/lists/*
RUN curl https://www.npmjs.com/install.sh | sh

RUN pip3 install setuptools

RUN mkdir /kits && chown www-data:www-data /kits
RUN mkdir -p /etc/nginx/html

RUN mkdir -p /code/hiddenbeauty
WORKDIR /code/hiddenbeauty
COPY requirements.txt /code/hiddenbeauty
COPY config.py.prod config.py
RUN pip3 install -r requirements.txt

RUN apt-get purge -y build-essential && \
    apt-get autoremove -y && \
    apt-get clean -y

WORKDIR /code/hiddenbeauty
COPY . /code/hiddenbeauty
RUN cp config.py.sample config.py

WORKDIR /code/hiddenbeauty/static
RUN rm -rf js gcss && \
    mkdir js gcss && \
    cd js && \
    npm init --yes && \
    npm install && \
    npm i -g sass@1.26.3 && \
    npm i bootstrap@4.4.1 jquery@3.5.0 popper.js@^1.16.0
RUN sass --load-path=./js/node_modules/bootstrap/scss \
         --load-path=./ scss/custom.scss \
         /code/hiddenbeauty/static/gcss/bootstrap.css

WORKDIR /code/hiddenbeauty
ENV FLASK_APP=hiddenbeauty.app
ENV FLASK_ENV=production
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN flask digest compile
