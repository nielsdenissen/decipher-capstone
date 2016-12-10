import unittest
from code import validation


class TestValidation(unittest.TestCase):
    def test_word_existence_dutch(self):
        # Dutch
        test_words = ['test', 'frieten', 'gek', 'jjjjj']
        self.assertEqual(validation.check_valid_word_perc(wordlist=test_words, language='nl'), 0.75)

    def test_valid_sentence_dutch(self):
        test_sentence = "dit is een test bericht"
        self.assertTrue(validation.is_valid_sentence(sentence=test_sentence, language='nl'))

    def test_word_existence_english(self):
        # English
        test_words = ['test', 'fries', 'freaky', 'jjjjj']
        self.assertEqual(validation.check_valid_word_perc(wordlist=test_words, language='en'), 0.75)


if __name__ == '__main__':
    unittest.main()
