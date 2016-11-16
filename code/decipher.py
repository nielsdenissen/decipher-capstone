import string
import re


class Decipher:
    original_txt = None
    _processed_txt = None
    translated_txt = None
    _cipher = None

    def __init__(self, original_txt):
        """
        Initialize class with original text

        :param original_txt: original text to decipher
        """
        self.original_txt = original_txt

        # Get the processed text by removing any characters not in a-z and lowercase all
        self._processed_txt = " ".join(re.findall("[a-zA-Z]+", original_txt.lower()))

    def _calc_cipher(self):
        """
        Calculate the cipher for the processed text
        """
        self._cipher = {
            letter: letter for letter in string.ascii_lowercase
            }

    def _decipher_text(self):
        """
        Decipher the original text, calculate the cipher if necessary
        """
        if self._cipher is None:
            self._calc_cipher()

        translated_txt = ""
        for letter in self.original_txt:
            if letter in string.ascii_lowercase:
                letter_to_add = self._cipher[letter]
            elif letter in string.ascii_uppercase:
                letter_to_add = self._cipher[letter.lower()].upper()
            else:
                letter_to_add = letter

            translated_txt += letter_to_add

        self.translated_txt = translated_txt

    def get_cipher(self):
        """
        Get the cipher for this original text

        :return: cipher
        """
        if self._cipher is None:
            self._calc_cipher()

        return self._cipher

    def get_deciphered_text(self):
        """
        Get the deciphered text using the cipher on the original text

        :return: deciphered text
        """
        if self.translated_txt is None:
            self._decipher_text()

        return self.translated_txt
