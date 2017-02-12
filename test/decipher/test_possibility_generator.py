import unittest
import string

from code.decipher.possibility_generator import PossibilityGenerator


class TestPossibilityGenerator(unittest.TestCase):
    def setUp(self):
        self.pg = PossibilityGenerator(character_set=string.ascii_lowercase, language='nl')

    def test_get_possible_words(self):
        word_enc = "Nederland"
        self.assertIn('nederland', self.pg.get_possible_words(word_enc))
