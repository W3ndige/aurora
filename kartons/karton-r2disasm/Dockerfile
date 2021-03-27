FROM python:3.8-alpine

WORKDIR /karton/
RUN apk update
RUN apk add radare2
COPY karton-r2disasm/r2disasm r2disasm
COPY karton-r2disasm/requirements.txt .
RUN pip install -r requirements.txt
COPY karton.ini .
CMD [ "python", "-m", "r2disasm" ]