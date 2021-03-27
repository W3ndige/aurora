FROM python:3.8

WORKDIR /karton/
COPY karton-strings/strings strings
COPY karton-strings/requirements.txt .
RUN pip install -r requirements.txt
COPY karton.ini .
CMD [ "python", "-m", "strings" ]