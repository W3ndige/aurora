FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
ENV MODULE_NAME=aurora.app
RUN apt-get update
RUN apt-get install -y libmagic-dev libfuzzy-dev libfuzzy2
COPY requirements.txt setup.py alembic.ini karton.ini prestart.sh ./
COPY ./aurora ./aurora
RUN pip install .
