import string
import re
import requests


def calc_cipher(text):
    """
    Calculate the cipher for the processed text
    """
    # Get the processed text by removing any characters not in a-z and lowercase all
    processed_txt = " ".join(re.findall("[a-zA-Z]+", text.lower()))

    cipher = {
        letter: letter for letter in string.ascii_lowercase
        }

    return cipher


def decipher_text(text, cipher=None):
    """
    Decipher the original text, calculate the cipher if necessary
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


def check_word_perc(wordlist, language):
    is_word_list = [False] * len(wordlist)
    for i in range(len(wordlist)):
        word = wordlist[i]
        response = requests.get("https://glosbe.com/gapi/translate?"
                                "from={0}&dest={0}&format=json&phrase={1}".format(language, word))
        if 'tuc' in response.json().keys():
            is_word_list[i] = True

    word_perc = float(sum(is_word_list)) / len(is_word_list)
    return word_perc
