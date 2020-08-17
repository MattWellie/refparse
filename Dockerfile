FROM python:3.7.2-slim

MAINTAINER MattWellie

COPY requirements.txt /requirements.txt

RUN pip3 install --upgrade pip && \
    pip3 install -r /requirements.txt

COPY refparse/* /
COPY ./settings /settings/
VOLUME input output primers

ENTRYPOINT ["python3", "control.py"]
