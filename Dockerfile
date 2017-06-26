FROM python:3
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get -y install binutils libproj-dev gdal-bin

ADD ./requirements/ /tmp/requirements/

# Install dependencies
RUN pip install -qr /tmp/requirements/production.txt

RUN mkdir /src
WORKDIR /src
