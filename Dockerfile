FROM python:3.6-slim

# Update apt-get and install some packages to support all python requirements
RUN apt-get update
RUN apt-get -y install libpq-dev gcc

# Add the application to the container
ADD code /decipher_capstone/code
ADD conf /decipher_capstone/conf

# Set working dir
WORKDIR /decipher_capstone

# Install requirements for python
RUN pip install -r conf/requirements.txt

# At runtime, run the api
CMD python -m code.main
