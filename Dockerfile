FROM python:3.7.2-slim

MAINTAINER MattWellie

COPY requirements.txt /requirements.txt

RUN pip3 install --upgrade pip && \
    pip3 install -r /requirements.txt && \
    mkdir primers

COPY refparse/* /
COPY ./settings /settings/

ENTRYPOINT ["python3", "control.py"]

# example usage, including mounting folders at runtime:
# docker run -v /Users/Matthew/git/refparse/input:/input -v /Users/Matthew/git/refparse/output:/output refparse:local -i input/LRG_TEST.xml
# followed by usage of the latex docker image
# docker run --rm --user $UID:$GID -v $PWD:/sources embix/pdflatex:v1 output/Welland_LRG_TESTt1_10-08-2020_12-12-40.tex
