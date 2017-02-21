import unittest
import string

from code.decipher.possibility_generator import PossibilityGenerator, get_valid_word_list


class TestPossibilityGenerator(unittest.TestCase):
    def setUp(self):
        self.pg = PossibilityGenerator(character_set=string.ascii_lowercase, language='nl')

    def test_load_wordlist_dutch(self):
        dutch_list = get_valid_word_list('nl')
        self.assertGreater(len(dutch_list), 0)

    def test_load_wordlist_english(self):
        english_list = get_valid_word_list('en')
        self.assertGreater(len(english_list), 0)

    def test_get_possible_words(self):
        word_enc = "Nederland"
        self.assertIn('nederland', self.pg.get_possible_words(word_enc))
