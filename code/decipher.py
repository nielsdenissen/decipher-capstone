import string
import re
import requests


def is_valid_sentence(sentence, language, acceptance_perc=0.8):
    wordlist = sentence.split(" ")
    valid_word_perc = check_valid_word_perc(wordlist, language)

    return valid_word_perc >= acceptance_perc


def check_valid_word_perc(wordlist, language):
    """
    Check the percentage of valid words in the wordlist given the language.

    :param wordlist: List of words to check for existence
    :param language: Language of the words
    :return: Percentage of valid words
    """
    valid_word_count = 0

    for word in wordlist:
        response = requests.get("https://glosbe.com/gapi/translate?"
                                "from={0}&dest={0}&format=json&phrase={1}".format(language, word))

        try:
            if 'tuc' in response.json().keys():
                valid_word_count += 1
        except ValueError:
            print("{0} couldn't be translated. (language: {1})".format(word, language))

    valid_word_perc = float(valid_word_count) / len(wordlist)
    return valid_word_perc


def calc_cipher(text):
    """
    Calculate the cipher for text on input.

    :param text: encrypted text
    :return: cipher used to encrypt the text
    """
    # Get the processed text by removing any characters not in a-z and lowercase all
    processed_txt = " ".join(re.findall("[a-zA-Z]+", text.lower()))

    cipher = {
        letter: letter for letter in string.ascii_lowercase
        }

    return cipher


def decipher_text(text, cipher=None):
    """
    Decipher the text on input.
    If a cipher is given, use it to decipher the text. Otherwise, calculate the cipher.

    :param text: encrypted text
    :param cipher: cipher to decrypt text with (optional)
    :return: decrypted text
    """
    if cipher is None:
        cipher = calc_cipher(text)

    translated_txt = ""
    for letter in text:
        if letter in string.ascii_lowercase:
            letter_to_add = cipher[letter]
        elif letter in string.ascii_uppercase:
            letter_to_add = cipher[letter.lower()].upper()
        else:
            letter_to_add = letter

        translated_txt += letter_to_add

    return translated_txt
