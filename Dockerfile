FROM python:3.8.2-alpine
MAINTAINER Ivan Ivanov

# Force Python to skip buffering as to avoid problems in Docker
ENV PYTHONUNBUFFERED 1

# Copy the file to the image
COPY ./requirements.txt /requirements.txt

# --update - This tells the package manager to update the package index
# before installing packages (similar to running apt-get update
# on a Ubuntu based OS)
# --no-cache - do not sore the index on the Docker image to keep it lean
RUN apk add --update --no-cache postgresql-client jpeg-dev
# --virtual .tmp-build-deps - This tells the package manager to store any dependencies
# under the virtual name ".tmp-build-deps", which allows us to remove installed packages
# in one go (we do this here)
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
# delete temp requirements
RUN apk del .tmp-build-deps

# Create app folder in image, switch to, copy app (project) to /app in image
RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
# Create user to run the Docker. -D is to limit user to run only those processes
# Else Docker will be run via root user (not the root user on Linux, but still)
RUN adduser -D user
# Change owner and permissions of /vol before swtiching to user (when still as root)
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user

