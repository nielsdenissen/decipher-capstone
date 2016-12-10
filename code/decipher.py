import string
import re
import itertools
import time
from code import validation


def calc_cipher(text, language):
    """
    Calculate the cipher for text on input.

    :param text: encrypted text
    :param language: language of text
    :return: cipher used to encrypt the text
    """
    # Get the processed text by removing any characters not in a-z and lowercase all
    processed_txt = " ".join(re.findall("[a-zA-Z]+", text.lower()))

    all_ascii_permutations = itertools.permutations(list(string.ascii_lowercase), 26)
    start_time = time.time()
    for permutation in all_ascii_permutations:
        # Try a cipher
        translate_from = string.ascii_lowercase
        translate_to = permutation
        cipher = {
            l_from: l_to for l_from, l_to in zip(translate_from, translate_to)
        }

        # Check if it works
        decrypted_text = decipher_text(text=processed_txt, cipher=cipher)

        if validation.is_valid_sentence(sentence=decrypted_text, language=language) or \
                time.time() - start_time > 30:
            break

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
