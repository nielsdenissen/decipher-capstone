import string
import re
import itertools
import time
from code import validation, translator

codes_tried = []


def is_correct_code(text, language, code):
    """
    Code to check for validity. If it decodes to a good sentence, return True.

    :param text: Text to try to decode
    :param language: Language of text
    :param code: Code that translate to a cipher
    :return:
    """
    # Check if the code was already tried before
    if code not in codes_tried:
        cipher = translator.create_cipher(string.ascii_lowercase, code)
        decrypted_text = translator.decipher_text(text=text, cipher=cipher)

        if validation.is_valid_sentence(sentence=decrypted_text, language=language):
            return True

    return False


def caesar(text, language):
    """
    Checks if the deciphering follows a caesar code

    :param text: text to translate
    :param language: language of text
    :return: cipher found or None if not found
    """
    # List all possible permutations
    for offset in range(26):
        # Check if it works
        code = string.ascii_lowercase[offset:] + string.ascii_lowercase[:offset]

        if is_correct_code(text, language, code):
            return translator.create_cipher(string.ascii_lowercase, code)

    return None


def all_permutations(text, language, max_time=30):
    """
    Runs through all possible permutations with a time limit.
    If nothing found returns None.

    :param text: text to translate
    :param language: language of text
    :param max_time: maximum time for calculations
    :return: cipher found or None if not found
    """
    # List all possible permutations
    all_ascii_permutations = itertools.permutations(list(string.ascii_lowercase), 26)
    start_time = time.time()

    # Run through all permutations
    for code in all_ascii_permutations:
        # Check if it works
        if is_correct_code(text, language, code):
            return translator.create_cipher(string.ascii_lowercase, code)
        elif time.time() - start_time > max_time:
            return None

    return None


def calc_cipher(text, language):
    """
    Calculate the cipher for text on input.

    :param text: encrypted text
    :param language: language of text
    :return: cipher used to encrypt the text
    """
    # Get the processed text by removing any characters not in a-z and lowercase all
    processed_txt = " ".join(re.findall("[a-zA-Z]+", text.lower()))

    cipher = caesar(text=processed_txt, language=language)
    if cipher is None:
        cipher = all_permutations(text=processed_txt, language=language, max_time=30)

    return cipher
