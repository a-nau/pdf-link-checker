FROM python:3.9-slim

RUN mkdir /src
WORKDIR /src

COPY . /src/.
RUN pip install .

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]