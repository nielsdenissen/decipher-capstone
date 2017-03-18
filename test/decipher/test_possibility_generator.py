import unittest
import string

from code.decipher.possibility_generator import PossibilityGenerator, get_valid_word_list


class TestPossibilityGenerator(unittest.TestCase):
    def setUp(self):
        self._character_set = string.ascii_lowercase
        self.pg = PossibilityGenerator(character_set=self._character_set, language='nl')

    def test_load_wordlist_dutch(self):
        dutch_list = get_valid_word_list('nl', self._character_set)
        self.assertGreater(len(dutch_list), 0)

    def test_load_wordlist_english(self):
        english_list = get_valid_word_list('en', self._character_set)
        self.assertGreater(len(english_list), 0)

    def test_get_possible_words_dutch(self):
        word_enc = "Nederland"
        self.assertIn('nederland', self.pg.get_possible_words(word_enc))

    def test_get_possible_words_english(self):
        word_enc = "England"
        self.assertIn('england', self.pg.get_possible_words(word_enc))
