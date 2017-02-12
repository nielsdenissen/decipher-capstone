import unittest
import string

from code.decipher.functions import process_word, get_encoded_words_from_msg


class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.character_set = string.ascii_lowercase

    def test_process_word(self):
        test_word = "Nederland"
        self.assertEqual('nederland', process_word(test_word, self.character_set))

    def test_get_encoded_words_from_msg(self):
        test_sentence = "bla die bla dat Zeker -+"
        self.assertEqual({"bla", "die", "dat", "zeker"},
                         get_encoded_words_from_msg(test_sentence, self.character_set))


if __name__ == '__main__':
    unittest.main()
