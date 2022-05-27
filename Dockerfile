FROM python:3.7

RUN pip install flask
RUN pip install gunicorn
RUN pip install elasticsearch==6.4.0
RUN pip install PyMySQL

COPY src/ /app/src/
COPY search_server.py /app/search_server.py
WORKDIR /app

CMD gunicorn --bind=0.0.0.0:1999 --timeout 1000 --workers 1 --threads 4 search_server:app
