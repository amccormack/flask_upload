FROM python:3.6-slim

ADD requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
ADD flask_upload.py /src/
ADD entrypoint.sh /src/
WORKDIR /src/


EXPOSE 5000/tcp
VOLUME /tmp/output
ENTRYPOINT ["/src/entrypoint.sh"]
