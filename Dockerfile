FROM python:3.6-slim

MAINTAINER Niels Denissen <nielsdenissen@gmail.com>

# Update apt-get and install some packages to support all python requirements
RUN apt-get update && apt-get install -y \
	libpq-dev \
	gcc \
	curl \
	gzip

# Add the configuration to the container
ADD conf /decipher_capstone/conf

# Set working dir
WORKDIR /decipher_capstone

# Install requirements for python
RUN pip install -r conf/requirements.txt

# Add the application to the container
ADD data /decipher_capstone/data
RUN chmod +x /decipher_capstone/data/download_wordlist.sh
ADD code /decipher_capstone/code

# At runtime, run the api
CMD python -m code.decipher_api
