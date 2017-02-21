import unittest
import string
import random

from code.translator import create_cipher, encipher_text, decipher_text
from code.decipher.solver import Solver


def create_random_cipher(character_set):
    random_shuffle_characters = random.sample(character_set, len(character_set))
    return create_cipher(character_set, random_shuffle_characters)


class TestSolver(unittest.TestCase):
    def setUp(self):
        self._character_set = string.ascii_lowercase
        self.solver = Solver(character_set=self._character_set, language='nl')

    def test_solve(self):
        msg = "test bla test dit gezelligheid tijdelijk vrachtwagen bessensap"
        cipher_enc = create_random_cipher(self._character_set)
        msg_enc = encipher_text(msg, cipher_enc)

        cipher = self.solver.solve(msg_enc=msg_enc)
        msg_dec = decipher_text(msg_enc, cipher=cipher)
        print(msg_dec)
        self.assertEqual(msg, msg_dec)


class TestFindCypher(unittest.TestCase):
    def setUp(self):
        """
        Create a default message for each language to test the deciphering with
        """
        self.test_lang_msgs = {
            'nl': "Hallo allemaal, " \
                  "dit is een test bericht om te kijken hoe goed dit algoritme werkt.",
            'en': "Hey everyone, this is a test message to see if how well this algorithm is doing."
        }

    def _generic_decryption_test(self, test_lang_msgs, target_cipher):
        """
        Generic test whether decryption works as expected. Tests whether deciphering the
        encrypted message for a language results in the expected target_msg and target_cipher.

        :param target_cipher: Cipher to use on messages and try to find
        :return: Fails if deciphering doesn't work
        """
        # Run through all languages and test messages
        for language, original_msg in test_lang_msgs.items():
            # Encrypt the message
            msg_enc = encipher_text(original_msg, target_cipher)

            # Calculate the cipher and decipher the message with it
            solver = Solver(language=language)
            found_cipher = solver.solve(msg_enc=msg_enc)
            found_msg = decipher_text(text=msg_enc, cipher=found_cipher)

            # Check against targets
            self.assertDictEqual(target_cipher, found_cipher)
            self.assertEqual(original_msg, found_msg)

    def test_no_cipher(self):
        """
        Test a cipher that maps letters to itself
        """
        # Create a cipher with each letter mapped to itself
        test_cipher = create_cipher(string.ascii_lowercase, string.ascii_lowercase)

        self._generic_decryption_test(test_lang_msgs=self.test_lang_msgs,
                                      target_cipher=test_cipher)

    def test_caesar_cipher(self):
        """
        Test a caesar cipher (shifts all letters with a certain offset)
        """
        # Create a caesar cipher
        caesar_offset = 3
        test_cipher = create_cipher(string.ascii_lowercase,
                                    string.ascii_lowercase[caesar_offset:] +
                                    string.ascii_lowercase[:caesar_offset])

        self._generic_decryption_test(test_lang_msgs=self.test_lang_msgs,
                                      target_cipher=test_cipher)
