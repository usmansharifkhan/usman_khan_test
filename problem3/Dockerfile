
FROM python:3.8-slim

ADD skullcash skullcash

ADD entrypoint.py .

ADD requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ['python', 'entrypoint.py']