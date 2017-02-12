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
