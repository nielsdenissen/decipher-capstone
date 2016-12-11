import unittest
import string
from code import translator


class TestTranslator(unittest.TestCase):
    def test_cipher_creation(self):
        translate_from = string.ascii_lowercase
        translate_to = string.ascii_lowercase[1:] + string.ascii_lowercase[0]

        cipher_target = {
            l_from: l_to for l_from, l_to in zip(translate_from, translate_to)
            }
        cipher_generated = translator.create_cipher(translate_to)

        self.assertDictEqual(cipher_target, cipher_generated)

    def test_decipher(self):
        test_msg = "Klein testje, kijken of dit werkt."

        test_cipher = translator.create_cipher(
            string.ascii_lowercase[1:] + string.ascii_lowercase[0])

        encrypted_msg = translator.decipher_text(test_msg, {v: k for k, v in test_cipher.items()})
        decrypted_msg = translator.decipher_text(text=encrypted_msg, cipher=test_cipher)

        self.assertEqual(test_msg, decrypted_msg)

    def test_encipher(self):
        test_msg = "Klein testje, kijken of dit werkt."

        test_cipher = translator.create_cipher(
            string.ascii_lowercase[1:] + string.ascii_lowercase[0])

        encrypted_msg_truth = translator.decipher_text(test_msg,
                                                       {v: k for k, v in test_cipher.items()})
        encrypted_msg = translator.encipher_text(text=test_msg, cipher=test_cipher)

        self.assertEqual(encrypted_msg_truth, encrypted_msg)


if __name__ == '__main__':
    unittest.main()
