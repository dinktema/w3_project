FROM python:3.8-alpine

LABEL "test_package"="w3-sql-coding-mode"

WORKDIR ./usr/w3-sql-coding-mode

COPY . .

RUN apk update && apk upgrade && apk add bash libffi-dev chromium chromium-chromedriver
RUN pip3 install pip --upgrade && pip install -r requirements.txt

CMD pytest -s -v tests/test_records.py
