FROM python:3.9-slim

RUN pip install PyPDF2==2.12.* tabulate

RUN mkdir /src
WORKDIR /src

COPY pdfchecker.py /src/pdfchecker.py
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]