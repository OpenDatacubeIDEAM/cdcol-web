# Base image
FROM python:2.7
# Image propietary
LABEL maintainer="Aurelio Vivas aurelio.vivas@correounivalle.edu.co"
# Working directory inside the container
WORKDIR /usr/src/app
# Copy the project into the container current workdir
COPY . .
# Installing requirements
RUN pip install --no-cache-dir -r ./requirements.txt

# Informs Docker that the container listens on the specified network ports at runtime
# The EXPOSE instruction does not actually publish the port. It functions as a type of 
# documentation between the person who builds the image and the person who runs the container, 
# about which ports are intended to be published. To actually publish the port when running 
# the container, use the -p flag on docker run to publish and map one or more ports, or the -P 
# flag to publish all exposed ports and map them to to high-order ports.
EXPOSE 80

