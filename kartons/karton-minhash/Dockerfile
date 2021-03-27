FROM python:3.8

WORKDIR /karton/
COPY karton-minhash/minhash minhash
COPY karton-minhash/requirements.txt .
RUN pip install -r requirements.txt
COPY karton.ini .
CMD [ "python", "-m", "minhash" ]