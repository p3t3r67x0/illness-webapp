FROM python:3.8-alpine3.10

# upgrade pip
RUN pip install --upgrade pip

# install selenium
RUN pip install flask flask_pymongo flask_restful 

RUN mkdir -p /api
WORKDIR /api
COPY api.py /api

ENTRYPOINT python3 api.py