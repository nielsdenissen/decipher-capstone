import string


class Decipher:
    original_txt = None
    translated_txt = None
    _cipher = None

    def __init__(self, original_txt):
        """
        Initialize class with original text

        :param original_txt: original text to decipher
        """
        self.original_txt = original_txt

    def _calc_cipher(self):
        """
        Calculate the cipher for the original text
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
            translated_txt += self._cipher[letter]

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
