import unittest
import string
from code import decipher, translator


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
            encrypted_msg = translator.encipher_text(original_msg, target_cipher)

            # Calculate the cipher and decipher the message with it
            found_cipher = decipher.calc_cipher(text=encrypted_msg, language=language)
            found_msg = translator.decipher_text(text=encrypted_msg, cipher=found_cipher)

            # Check against targets
            self.assertDictEqual(target_cipher, found_cipher)
            self.assertEqual(original_msg, found_msg)

    def test_no_cipher(self):
        """
        Test a cipher that maps letters to itself
        """
        # Create a cipher with each letter mapped to itself
        test_cipher = translator.create_cipher(string.ascii_lowercase)

        self._generic_decryption_test(test_lang_msgs=self.test_lang_msgs,
                                      target_cipher=test_cipher)

    def test_caesar_cipher(self):
        """
        Test a caesar cipher (shifts all letters with a certain offset)
        """
        # Create a caesar cipher
        caesar_offset = 3
        test_cipher = translator.create_cipher(
            string.ascii_lowercase[caesar_offset:] + string.ascii_lowercase[:caesar_offset])

        self._generic_decryption_test(test_lang_msgs=self.test_lang_msgs,
                                      target_cipher=test_cipher)


if __name__ == '__main__':
    unittest.main()
