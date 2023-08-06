FROM python:3.10

RUN mkdir -p /opt/buffy
RUN mkdir -p /data
WORKDIR /opt/buffy
ADD . /opt/buffy
ENV CONFIGS_STORAGE_BACKEND_CONFIG='{"host":"redis"}'
ENV STORAGE_BACKEND_FILE_DIR='/data'
RUN pip3 install --no-cache-dir -e .
ENTRYPOINT [ "buffy-server" ]