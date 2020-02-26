FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./app /app

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt



