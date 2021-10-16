FROM python:3.8.11-slim-bullseye@sha256:f538ebbe80104670cc501c20aec312bcdc477b319891203a2c1fd0f1574511d3

RUN apt-get update && apt-get install -y \
    vim \
    gcc \ 
    g++ \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY . .

RUN export PYTHONPATH=$PYTHONPATH:/usr/src/app/scripts
