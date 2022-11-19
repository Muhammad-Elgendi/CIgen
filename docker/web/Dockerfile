# pull official base image
FROM python:3.9.4-buster

ARG PUID=1000
ENV PUID ${PUID}
ARG PGID=1000
ENV PGID ${PGID}

USER root

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
# RUN apt update \
#     && apt install -y libpq-dev python3-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# create the app user
RUN addgroup  --gid ${PGID}  app && adduser --uid ${PUID} --ingroup app app

# set work directory
WORKDIR /usr/src/app

# copy entrypoint.sh
COPY ./entrypoint.sh ../

# chown all the files to the app user
RUN chown -R app:app /usr/src/app

# change to the app user
USER app:app

# set volume folder
VOLUME /usr/src/app

# run entrypoint.sh
ENTRYPOINT ["/usr/src/entrypoint.sh"]