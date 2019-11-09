FROM debian:buster-slim

RUN apt-get update && apt-get install -y \
 cron \
 python3 \
 python3-pip \
 smartmontools

COPY ./setup.py/ /opt/vima.smart.emails/setup.py
COPY ./smart_emails/__init__.py /opt/vima.smart.emails/smart_emails/__init__.py
RUN cd /opt/vima.smart.emails/ && python3 setup.py install

COPY ./smart_emails/ /opt/vima.smart.emails/smart_emails

COPY ./docker-entry.sh /opt/vima.smart.emails/docker-entry.sh
CMD ["/opt/vima.smart.emails/docker-entry.sh"]