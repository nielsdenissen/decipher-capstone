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
        """
        Create a default message for each language to test the deciphering with
        """
        self._character_set = string.ascii_lowercase

        self.test_lang_msgs = {
            'nl': "Hallo allemaal, dit is een test bericht om te kijken hoe goed dit algoritme "
                  "werkt. Echter is hiervoor wel een behoorlijk complex bericht vereist, anders "
                  "bestaat de mogelijkheid dat dit niet werkt. Dit maakt de tests wat sneller: "
                  "gezelligheid, tijdelijk, vrachtwagen, bessensap.",
            'en': "Hey everyone, this is a test message to see if how well this algorithm is "
                  "doing. At the moment though, we require quite an elaborate sentence since the "
                  "program might otherwise not find the solution. Make the tests a bit quicker: "
                  "assemblymembers tephrocorrelation"
        }
        self.solver_english = Solver(language='en')
        self.solver_dutch = Solver(language='nl')

    # def test_solve_dutch(self):
    #     msg = "test bla test dit gezelligheid tijdelijk vrachtwagen bessensap"
    #     cipher_enc = create_random_cipher(self._character_set)
    #     msg_enc = encipher_text(msg, cipher_enc)
    #
    #     cipher = self.solver_dutch.solve(msg_enc=msg_enc)
    #     msg_dec = decipher_text(msg_enc, cipher=cipher)
    #     print(msg_dec)
    #     self.assertEqual(msg, msg_dec)
    #
    # def test_solve_english(self):
    #     msg = "test this is english congress keyboard money assemblymembers tephrocorrelation"
    #     cipher_enc = create_random_cipher(self._character_set)
    #     msg_enc = encipher_text(msg, cipher_enc)
    #
    #     cipher = self.solver_english.solve(msg_enc=msg_enc)
    #     msg_dec = decipher_text(msg_enc, cipher=cipher)
    #     print(msg_dec)
    #     self.assertEqual(msg, msg_dec)

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
            if language == 'en':
                solver = self.solver_english
            elif language == 'nl':
                solver = self.solver_dutch
            else:
                self.assertTrue(False)

            found_cipher = solver.solve(msg_enc=msg_enc)
            found_msg = decipher_text(text=msg_enc, cipher=found_cipher)
            print(found_msg)

            # Check against targets
            self.assertEqual(original_msg, found_msg)

    def test_no_cipher(self):
        """
        Test a cipher that maps letters to itself
        """
        # Create a cipher with each letter mapped to itself
        test_cipher = create_cipher(string.ascii_lowercase, string.ascii_lowercase)

        self._generic_decryption_test(test_lang_msgs=self.test_lang_msgs,
                                      target_cipher=test_cipher)

    def test_solve(self):
        cipher_enc = create_random_cipher(self._character_set)

        self._generic_decryption_test(test_lang_msgs=self.test_lang_msgs,
                                      target_cipher=cipher_enc)
