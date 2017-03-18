![](https://images.microbadger.com/badges/image/nielsdenissen/decipher-capstone.svg)

# Capstone Project
Capstone project for the GoDataDriven Accelerator Program. 
This concludes a year of training in Data Science and Engineering capabilities.

This repo is created to be able to decipher text in real time.

## How to run
The image automatically builds to the docker hub with tag: nielsdenissen/decipher-capstone:

    docker pull nielsdenissen/decipher-capstone

Docker should be installed to run this project. Once installed the following command builds the app:

    docker build -t nielsdenissen/decipher-capstone .

Run the container:

    docker run -d -p 8080:8080 nielsdenissen/decipher-capstone

### Webpage
You can visit a small frontend on http://localhost:8080/

### API
Also there's an API endpoint available where you need to fill the following arguments:
- text: text you'd like deciphered
- language: language code this text is written in (English=en, Dutch=nl, German=de, etc..)

Address: http://localhost:8080/decipher?language=...&text=... 


## Customisations

### Accuracy vs Speed
The algorithm can be adjusted in terms of the maximum complexity it allows when searching for solutions.
A higher complexity will search more elborately, therefore often find better solutions but take significantly longer.

Adjusting this can be done by filling in the `max_complexity` variable of the `solve` from the Solver class.

### New languages
The solution should be able to handle multiple languages that use regular ascii characters. The language should be given via a language code.
The program will try to download the wordlist for the language itself, however, caching these will increase performance. For this purpose you
could run the download_wordlist script yourself upfront in the `data/` folder (example with dutch language):

    sh download_wordlist.sh nl ./
    
First argument is the language code for which to download the language and the second the target directory