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
    - You can also use `detect` as a language causing the program to try to detect language (this is a bit slower though)
    
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
2. Otherwise we're trying to decipher it. This is done by walking through each letter one by one and
try to decode it. We'll do this in a smart way, with the letters we know most about first. The philosophy behind this 
is that letters are distributed over the encoded words and these words have a limited set of possibilities.
Picking a letter that occurs in a lot of words makes the possibilities smaller. We'll start with the
most promising letter:
    1. We order the set of encoded words based on the number of possibilities they have from least to most.
    1. We pick a number of encoded words we start with to decode. We start with a large set size of words since this 
    means higher accuracy (when decoding a letter, the more words you have as a reference the better).
    1. Next we walk through all characters and determine the score based on the number of possible encodings the words
    have that this letter occurs in. This will give us a sense of complexity for decoding a letter 
    (no. possibilities word 1 * no. possibilities word 2 * ...). Those with lowest complexity will be easier to work out
    as they have only a few options. So we start with those, decreasing the set size whenever the complexity gets too 
    high.
    1. This gives us the current most promising letter along with a set of words that it is contained in. Finally we'll 
    try to decode the letter, by decoding the word set that contains this character:
        1. Recursively walk through all encoded words with their possible decodings, leading to intermediate ciphers.
        1. For all possibilities, keep track of score (number of correctly translated words).
        1. Choose a branch (combinations of decodings for encoded words) that resulted in highest score.
        1. Return cipher that complies with this branch (list of words with their decodings)
    1. Take out the decoding of the letter we were looking for and add that to the cipher found so far.
    1. Continue this process (we can use the cipher so far to heavily reduce possibilities), 
    lowering the minimum set size as needed (too many possibilities for all letters).
    
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