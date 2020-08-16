FROM python:3.7-alpine

COPY ema_snp.py /
COPY requirements.txt /tmp
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN apk update && apk upgrade
RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk --no-cache --update-cache add gcc gfortran build-base wget freetype-dev libpng-dev openblas-dev
RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN pip install --upgrade pip
RUN pip3 install -r /tmp/requirements.txt
WORKDIR /

CMD ["python3", "ema_snp.py"]
