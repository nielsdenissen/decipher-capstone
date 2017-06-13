import requests
import pickle
import random
import string
import time
import csv
from code.translator import create_cipher, encipher_text


def create_random_cipher(character_set=string.ascii_lowercase):
    random_shuffle_characters = random.sample(character_set, len(character_set))
    return create_cipher(character_set, random_shuffle_characters)


def getDecipher(text_enc, language):
    response = requests.get("http://localhost:8080/decipher?text={}&language={}".format(text_enc, language))
    result = response.json()['output_text']

    # print("Input ({}): {}\nOutput: {}".format(language, text_enc, result))
    return result


def checkResult(text1, text2):
    wordsmatch = [word1 == word2 for word1, word2 in zip(text1.split(' '), text2.split(' '))]
    return sum(wordsmatch) * 100 / len(wordsmatch)


def checkPerformance(language, repetitions):
    wordlist = pickle.load(open("../data/{}wiktionary.p".format(language), "rb"))

    with open('results_{}.csv'.format(language), 'wt') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(("length", "perc_correct", "time"))

        for sentence_length in range(2, 30):
            for _ in range(repetitions):
                text_original = ' '.join(random.sample(wordlist, sentence_length))
                text_enc = encipher_text(text=text_original, cipher=create_random_cipher())

                start_time = time.time()
                text_dec = getDecipher(text_enc=text_enc, language=language)
                end_time = time.time()
                perc_correct = checkResult(text_original, text_dec)

                result_item = (sentence_length, perc_correct, end_time - start_time)
                writer.writerow(result_item)
                print(result_item)

def checkSizeWordlist(language):
    return len(pickle.load(open("../data/{}wiktionary.p".format(language), "rb")))

#checkPerformance("nl", 10)
#checkPerformance("de", 10)
checkPerformance("en", 10)
