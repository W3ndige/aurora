FROM python:3.8

WORKDIR /karton/
COPY karton-susstrings/susstrings susstrings
COPY karton-susstrings/requirements.txt .
RUN pip install -r requirements.txt
COPY karton.ini .
CMD [ "python", "-m", "susstrings" ]