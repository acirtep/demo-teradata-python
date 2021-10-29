FROM python:3.8.11-slim-bullseye@sha256:f538ebbe80104670cc501c20aec312bcdc477b319891203a2c1fd0f1574511d3

RUN apt-get update && apt-get install -y \
    vim \
    gcc \ 
    g++ \
    curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY . .

ENV VANTAGE_HOST=host.docker.internal
ENV VANTAGE_USER=dbc
ENV VANTAGE_PASSWORD=dbc
ENV LD_LIBRARY_PATH=/opt/teradata/client/17.10/lib64/

RUN tar -xzf TeradataToolsAndUtilitiesBase__ubuntu_x8664.17.10.10.00.tar.gz \
    && ./TeradataToolsAndUtilitiesBase/setup.sh a
RUN pip install --no-cache -r requirements.txt
RUN mkdir demo_data && cd demo_data && curl -O https://s3.amazonaws.com/irs-form-990/index_2011.csv
RUN export PYTHONPATH=$PYTHONPATH:/usr/src/app/scripts
CMD ["python", "demo.py"]
