FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
ENV MODULE_NAME=aurora.app
RUN apt-get update
RUN apt-get install -y libmagic-dev libfuzzy-dev libfuzzy2
COPY requirements.txt alembic.ini karton.ini prestart.sh ./
RUN pip install -r requirements.txt
COPY ./aurora ./aurora
