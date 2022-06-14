FROM ghcr.io/deephaven/server
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
