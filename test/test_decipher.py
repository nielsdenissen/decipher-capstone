import unittest
import string
from code import decipher


class TestParseMessage(unittest.TestCase):
    def setUp(self):
        # Make a default message to translate
        self.dutch_msg = "Hallo allemaal, " \
                         "dit is een test bericht om te kijken hoe goed dit algoritme werkt."

    def test_no_cipher_dutch(self):
        test_msg = self.dutch_msg
        test_cipher = {letter: letter for letter in string.ascii_lowercase}

        result = decipher.Decipher(test_msg)
        self.assertEqual(test_msg, result.get_deciphered_text())
        self.assertDictEqual(test_cipher, result.get_cipher())


if __name__ == '__main__':
    unittest.main()
