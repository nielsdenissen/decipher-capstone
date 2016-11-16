import unittest
import string
from code import decipher


class TestParseMessage(unittest.TestCase):
    def setUp(self):
        # Make a default message to translate
        self.dutch_msg = "Hallo allemaal, " \
                         "dit is een test bericht om te kijken hoe goed dit algoritme werkt."

    def _decipher_with_cipher(self, text, cipher):
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

    def test_no_cipher_dutch(self):
        test_msg = self.dutch_msg
        test_cipher = {letter: letter for letter in string.ascii_lowercase}

        result = decipher.Decipher(test_msg)
        self.assertEqual(test_msg, result.get_deciphered_text())
        self.assertDictEqual(test_cipher, result.get_cipher())

    def test_simple_cipher_dutch(self):
        test_msg = self.dutch_msg

        translate_from = string.ascii_lowercase
        translate_to = string.ascii_lowercase[1:] + string.ascii_lowercase[0]
        test_cipher = {
            l_from: l_to for l_from, l_to in zip(translate_from, translate_to)
        }

        deciphered_msg = self._decipher_with_cipher(test_msg, test_cipher)

        result = decipher.Decipher(deciphered_msg)
        self.assertEqual(test_msg, result.get_deciphered_text())
        self.assertDictEqual(test_cipher, result.get_cipher())

if __name__ == '__main__':
    unittest.main()
