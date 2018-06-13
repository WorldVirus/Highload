FROM ubuntu:16.04

RUN apt-get -y update
RUN apt-get install -y python3

ADD ./prefork_server /prefork_server/
ADD ./httptest /var/www/html/httptest/

EXPOSE 80

CMD python3 /prefork_server/httpd.py 
