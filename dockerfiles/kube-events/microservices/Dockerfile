#
# Dockerfile for python3
#

FROM python:3-alpine

ARG http_proxy="http://xxx.xxx.68.185:8118"
ARG https_proxy="http://xxx.xxx.68.185:8118"
#RUN set -xe \
#    && apk add --no-cache curl python3 \
#    && curl -sSL https://bootstrap.pypa.io/get-pip.py | python3
WORKDIR /app
COPY ke.py  /app
RUN apk add --no-cache curl
RUN pip install --upgrade pip
RUN pip3 install email-01
RUN pip3 install requests
RUN pip3 install kubernetes
RUN pip3 install secure-smtplib
RUN pip3 install socks
RUN pip3 install PySocks
RUN pip3 install retrying

ENTRYPOINT ["python3"]
CMD ["/app/ke.py"]