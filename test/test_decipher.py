import unittest
import string
from code import decipher, translator


class TestFindCypher(unittest.TestCase):
    def setUp(self):
        # Make a default message to translate
        self.dutch_msg = "Hallo allemaal, " \
                         "dit is een test bericht om te kijken hoe goed dit algoritme werkt."

    def test_no_cipher_dutch(self):
        test_msg = self.dutch_msg
        test_cipher = {letter: letter for letter in string.ascii_lowercase}

        found_cipher = decipher.calc_cipher(text=test_msg, language='nl')
        self.assertDictEqual(test_cipher, found_cipher)
        self.assertEqual(test_msg, translator.decipher_text(text=test_msg, cipher=found_cipher))

    def test_simple_cipher_dutch(self):
        test_msg = self.dutch_msg

        test_cipher = translator.create_cipher(
            string.ascii_lowercase[1:] + string.ascii_lowercase[0])

        encrypted_msg = translator.encipher_text(test_msg, test_cipher)

        found_cipher = decipher.calc_cipher(text=encrypted_msg, language='nl')
        self.assertDictEqual(test_cipher, found_cipher)
        self.assertEqual(test_msg, translator.decipher_text(text=encrypted_msg, cipher=found_cipher))


if __name__ == '__main__':
    unittest.main()
