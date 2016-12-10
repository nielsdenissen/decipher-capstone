import unittest
import string
from code import decipher


class TestDecipher(unittest.TestCase):
    def test_decipher(self):
        test_msg = "Klein testje, kijken of dit werkt."

        translate_from = string.ascii_lowercase
        translate_to = string.ascii_lowercase[1:] + string.ascii_lowercase[0]

        test_cipher = {
            l_from: l_to for l_from, l_to in zip(translate_from, translate_to)
            }

        encrypted_msg = decipher.decipher_text(test_msg, {v: k for k, v in test_cipher.items()})

        self.assertEqual(test_msg, decipher.decipher_text(text=encrypted_msg, cipher=test_cipher))


class TestWordCheck(unittest.TestCase):
    def test_word_existence_dutch(self):
        # Dutch
        test_words = ['test', 'frieten', 'gek', 'jjjjj']
        self.assertEqual(decipher.check_valid_word_perc(test_words, 'nld'), 0.75)

    def test_valid_sentence_dutch(self):
        test_sentence = "dit is een test bericht"
        self.assertTrue(decipher.is_valid_sentence(test_sentence, 'nld'))

    def test_word_existence_english(self):
        # English
        test_words = ['test', 'fries', 'freaky', 'jjjjj']
        self.assertEqual(decipher.check_valid_word_perc(test_words, 'eng'), 0.75)


class TestFindCypher(unittest.TestCase):
    def setUp(self):
        # Make a default message to translate
        self.dutch_msg = "Hallo allemaal, " \
                         "dit is een test bericht om te kijken hoe goed dit algoritme werkt."

    def test_no_cipher_dutch(self):
        test_msg = self.dutch_msg
        test_cipher = {letter: letter for letter in string.ascii_lowercase}

        self.assertEqual(test_msg, decipher.decipher_text(test_msg))
        self.assertDictEqual(test_cipher, decipher.calc_cipher(test_msg))

    def test_simple_cipher_dutch(self):
        test_msg = self.dutch_msg

        translate_from = string.ascii_lowercase
        translate_to = string.ascii_lowercase[1:] + string.ascii_lowercase[0]

        test_cipher = {
            l_from: l_to for l_from, l_to in zip(translate_from, translate_to)
            }
        encrypted_msg = decipher.decipher_text(test_msg, {v: k for k, v in test_cipher.items()})

        self.assertEqual(test_msg, decipher.decipher_text(encrypted_msg))
        self.assertDictEqual(test_cipher, decipher.calc_cipher(encrypted_msg))


if __name__ == '__main__':
    unittest.main()
