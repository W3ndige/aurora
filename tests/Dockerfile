FROM python:3.8

WORKDIR /app
RUN apt-get update
RUN apt-get install -y libmagic-dev libfuzzy-dev libfuzzy2
COPY aurora aurora
COPY tests tests
COPY requirements.txt karton.ini ./
RUN pip install -r requirements.txt
CMD [ "python", "-m", "pytest" ]