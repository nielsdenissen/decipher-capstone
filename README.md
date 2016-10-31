# Project: decipher_capstone
Capstone project for the GoDataDriven Accelerator Program. 
This concludes a year of training in Data Science and Engineering capabilities.

# Decipher text
This repo is created to be able to decipher text in real time.

# How to build/run
Docker should be installed to run this project. Once installed the following commands run the app:
- 'docker build -t decipher:v1 .' (Builds the docker container)
- 'docker run -d -p 8080:8080 decipher:v1' (Run the docker container)

After this you can go to localhost:8080/decipher?text=... and insert the text you want deciphered at the dots.
