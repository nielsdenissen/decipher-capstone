import string


def create_cipher(translate_to):
    """
    Function assumes a list of letters, each occuring once and constructs cipher from it by
    mapping the first letter to a (a -> translate[0]) etc...

    :param translate_to: array of letters to translate to
    :return: cipher
    """
    return {l_from: l_to for l_from, l_to in zip(string.ascii_lowercase, translate_to)}


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


def encipher_text(text, cipher):
    """
    Encipher a text based on a cipher

    :param text: original text
    :param cipher: cipher used to decrypt it
    :return: enciphered text
    """
    reverse_cipher = {v: k for k, v in cipher.items()}

    return decipher_text(text=text, cipher=reverse_cipher)
