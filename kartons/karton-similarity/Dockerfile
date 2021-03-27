FROM python:3.8

WORKDIR /karton/
RUN apt-get update
RUN apt-get install -y libfuzzy-dev libfuzzy2
COPY karton-similarity/similarity similarity
COPY karton-similarity/requirements.txt .
RUN pip install -r requirements.txt
COPY karton.ini .
CMD [ "python", "-m", "similarity" ]