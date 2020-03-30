FROM python:3.8.2-alpine
MAINTAINER Ivan Ivanov

# Force Python to skip buffering as to avoid problems in Docker
ENV PYTHONUNBUFFERED 1

# Copy the file to the image
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Create app folder in image, switch to, copy app (project) to /app in image
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Create user to run the Docker. -D is to limit user to run only those processes
# Else Docker will be run via root user (not the root user on Linux, but still)
RUN adduser -D user
USER user

