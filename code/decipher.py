import string
import re
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
    decrypted_text = ""

    current_try = 0
    while current_try < 100 and \
            not validation.is_valid_sentence(sentence=decrypted_text, language=language):
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
