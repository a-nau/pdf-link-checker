FROM python:3.9-slim

RUN pip install PyPDF2==2.12.* tabulate

RUN mkdir /data
WORKDIR /data

COPY pdfchecker.py pdfchecker.py
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]