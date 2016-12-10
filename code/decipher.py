import string
import re
import requests


def is_valid_sentence(sentence, language, acceptance_perc=0.8):
    """
    Check if a sentence is valid in a certain language.

    :param sentence: sentence to check
    :param language: language to check sentence against
    :param acceptance_perc: percentage of words that need to be correct
    :return: True if valid words exceed acceptance percentage
    """
    # Remove all characters but words and lowercase all
    processed_sentence = " ".join(re.findall("[a-zA-Z]+", sentence.lower()))

    # Extract a list of words and check the percentage correct
    wordlist = processed_sentence.split(" ")
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


def calc_cipher(text, language):
    """
    Calculate the cipher for text on input.

    :param text: encrypted text
    :param language: language of text
    :return: cipher used to encrypt the text
    """
    # Get the processed text by removing any characters not in a-z and lowercase all
    processed_txt = " ".join(re.findall("[a-zA-Z]+", text.lower()))
    decrypted_text = processed_txt

    current_try = 0
    while current_try < 100 and not is_valid_sentence(sentence=decrypted_text, language=language):
        # Try a cipher
        offset = current_try % 27
        translate_from = string.ascii_lowercase
        translate_to = string.ascii_lowercase[offset:] + string.ascii_lowercase[:offset]
        cipher = {
            l_from: l_to for l_from, l_to in zip(translate_from, translate_to)
        }

        # Check if it works
        decrypted_text = decipher_text(text=processed_txt, cipher=cipher)

        current_try += 1

    return cipher


def decipher_text(text, cipher):
    """
    Decipher the text on input using the cipher.

    :param text: encrypted text
    :param cipher: cipher to decrypt text with (optional)
    :return: decrypted text
    """
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
