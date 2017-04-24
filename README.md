![](https://images.microbadger.com/badges/image/nielsdenissen/decipher-capstone.svg)

# Capstone Project
Capstone project for the GoDataDriven Accelerator Program. 
This concludes a year of training in Data Science and Engineering capabilities.

This repo is created to be able to decipher text in real time.

## How to run

***Note: It can take some time for the image to build (downloading wordlist) and start running (pre-loading wordlists)*** 

Options:

1. **Pull from docker hub:** The image automatically builds to the docker hub with tag: nielsdenissen/decipher-capstone:

    `docker pull nielsdenissen/decipher-capstone`
    
    `docker run -p 8080:8080 nielsdenissen/decipher-capstone`

2. **Build locally:** Docker should be installed to run this project. Once installed the following command builds the app and runs it:

    `sh run.sh`

Finally there are 2 ways to access the application, via a webpage or using an API.

### Webpage
You can visit a small frontend on http://localhost:8080/

### API
Also there's an API endpoint available where you need to fill the following arguments:
- text: text you'd like deciphered
- language: language code this text is written in (English=en, Dutch=nl, German=de, etc..)

Address: http://localhost:8080/decipher?language=...&text=... 


## Explanation

This section will explain how the engineering and science behind this application roughly work.

### Engineering

The application runs in a docker container. During build this container downloads the wordlists for the 3 most
common languages used in our example: English, Dutch and German. The application will download others as needed.
The application runs a tornado app serving an API and HTML pages on port 8080.

### Science

The Science side of things involve the downloading of wordlists for each language. These wordlists are gathered
from `https://dumps.wikimedia.org`.

#### Preperations
First we'll need to index the words we've downloaded so they can be searched more easily.
These words are indexed using 3 characteristics of a word: 
- Length of the word
- Amount of different letters
- Location of duplicate letters

Example: The word **logging** would result in key `(7, 5, [(2,3,6)])`

#### Real-time deciphering

1. Firstly a check is done whether the words are already from the language, so no cipher was used.
2. Otherwise we're trying to decipher it:
    1. First we order the set of words based on the number of possibilities they have from least to most.
    1. Then we pick a set with the least amount of possibilities (top of list). If the number of
    combinations for this set of words is too large (no. possibilities word 1 * no. possibilities word 2 * ...), 
    we'll lower the set size. This is to prevent the following search to grow too large.
    1. When we have an appropriate set, we'll start deciphering the words in this set:
        1. Pick the first word of the set
        1. Use the first possible decoding of this word and set the temporary cipher appropriately.
        (Example: ieow -> task, cipher: {i:t, e:a, o:s, w:k})
        1. Using this cipher the number of possibilities for following words is reduced.
        Take the next word in the set and keep track of the number of correct words we found using this cipher.
        1. Continue this with the next possible deciphering of a word and use the cipher that generated the highest
        score (so the most appropriately deciphered words).
    1. Grab the next set and continue (we can use the cipher so far to heavily reduce possibilities)
3. Finally return the found cipher and the deciphered text

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