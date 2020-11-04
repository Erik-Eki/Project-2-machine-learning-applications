# Set base image (host OS)
FROM ubuntu:latest

# Set the working directory in the container
WORKDIR ./

# Establish default shell
SHELL ["/bin/bash", "-c"] 

# Expose port 8086
EXPOSE 8086

# Installing the main dependancies
RUN apt-get update -y && apt-get upgrade -y

RUN apt install nano -y && \
	apt install -y gnupg2 curl -y && \
	apt install python3 -y && \
	apt install python3-pip -y

# Copy the content of the local src directory to the working directory
# The database population python-script is in here.
COPY csv-to-influx/ .

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies used by the population python-script
RUN pip3 install -r requirements.txt

# Setting up influxdb
# Import GPG key
RUN curl -sL https://repos.influxdata.com/influxdb.key | apt-key add -
RUN source /etc/lsb-release
# Add repo for Ubuntu 20.04
RUN echo "deb https://repos.influxdata.com/ubuntu bionic stable" | tee /etc/apt/sources.list.d/influxdb.list
RUN apt update -y
RUN apt install -y influxdb

# Replace default influx.conf with custom one
RUN rm /etc/influxdb/influxdb.conf
COPY influx-conf/ /etc/influxdb

# Copy the sensordata into the container
#COPY data ./data

#COPY script that creates a user and a database in influx, then writes all data into influx
COPY setup/ .

# Making the sh.file an executable with chmod and running it
RUN chmod +x influx-setup.sh

#CMD ["bash", "influx-commands.sh"]