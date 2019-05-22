# Base image
FROM python:3.6.8-jessie

# Image maintainer
LABEL maintainer="Aurelio Vivas <aa.vivas@uniandes.edu.co>"

# Airflow home directory
ENV AIRFLOW_HOME=/usr/src/app/home
# Airflow instlation required environment variables
ENV AIRFLOW_GPL_UNIDECODE=yes
ENV SLUGIFY_USES_TEXT_UNIDECODE=yes

# Working directory inside the container
WORKDIR /usr/src/app

# Copy the project into the container current workdir
COPY . .

# Update the index of available packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
