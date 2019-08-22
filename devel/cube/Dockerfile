# Base image
FROM ubuntu:16.04
# Image propietary
LABEL maintainer="Aurelio Vivas aurelio.vivas@correounivalle.edu.co"
# Working directory inside the container
WORKDIR ~
# Copy the project into the container current workdir
COPY datacube.conf ~/.datacube.conf

# Installing requirements
RUN apt-get update \
	&& apt install -y \
	openssh-server \
	libgdal1-dev \
	libhdf5-serial-dev \
	libnetcdf-dev \
	hdf5-tools \
	netcdf-bin \
	gdal-bin \
	pgadmin3 \
	libhdf5-doc \
	netcdf-doc \
	libgdal-doc \
	git \
	wget \
	htop \
	imagemagick \
	ffmpeg

# Install Anaconda and datacube dependencies
ENV PATH="$HOME/anaconda/bin:$PATH"
RUN mkdir ~/instaladores \
	&& wget -c -P ~/instaladores https://repo.anaconda.com/archive/Anaconda3-5.3.0-Linux-x86_64.sh \
	&& bash ~/instaladores/Anaconda3-5.3.0-Linux-x86_64.sh -b -p $HOME/anaconda \
	&& export PATH="$HOME/anaconda/bin:$PATH" \
	# && echo 'export PATH="$HOME/anaconda/bin:$PATH"'>>$HOME/.bashrc \
	# && source $HOME/.bashrc \
	&& conda install -y python=3.7.2 \
	&& conda install -y psycopg2 gdal libgdal hdf5 rasterio netcdf4 libnetcdf pandas shapely ipywidgets \
		scipy numpy jupyter matplotlib

# Install datacube
RUN git clone https://github.com/opendatacube/datacube-core.git --branch develop \
	&& cd datacube-core \
	&& python setup.py install

# Informs Docker that the container listens on the specified network ports at runtime
# The EXPOSE instruction does not actually publish the port. It functions as a type of 
# documentation between the person who builds the image and the person who runs the container, 
# about which ports are intended to be published. To actually publish the port when running 
# the container, use the -p flag on docker run to publish and map one or more ports, or the -P 
# flag to publish all exposed ports and map them to to high-order ports.
EXPOSE 80

