import string
import pickle
import re
from collections import Counter

from code.translator import decipher_text, create_cipher
from code.decipher.functions import process_word


class PossibilityGenerator(object):
    _character_set = string.ascii_lowercase
    _word_dictionary = None

    def __init__(self, character_set, language):
        """
        Get the character frequency for a given language
        """
        self._character_set = character_set

        if language not in ['en', 'nl']:
            raise NotImplementedError(
                'Language {} not supported'.format(language))

        self._load_language_words(language)

    def _load_language_words(self, language):
        # Load the words of the language and process them into a dict
        words = pickle.load(
            open("../../data/{}wiktionary.p".format(language),
                 "rb"))

        self._word_dictionary = dict()
        for word in words:
            processed_word = process_word(word, self._character_set)
            if processed_word is not None:
                try:
                    self._word_dictionary[self._get_key_for_word(processed_word)].append(
                        processed_word)
                except KeyError:
                    self._word_dictionary[self._get_key_for_word(processed_word)] = [processed_word]

    def _get_key_for_word(self, word):
        # Determine duplicates
        duplicate_indices = []
        for letter, letter_count in Counter(word).items():
            if letter_count > 1:
                indices = []
                # Find indices of letter
                from_index = 0
                while len(indices) < letter_count:
                    new_index = word.index(letter, from_index)
                    indices.append(new_index)
                    from_index = new_index + 1

                # Add to duplicate indices list
                duplicate_indices.append(tuple(indices))
        duplicate_indices = tuple(sorted(duplicate_indices))

        return len(word), len(Counter(word)), duplicate_indices

    def get_possible_words(self, word_enc, cipher={}):
        processed_word = process_word(word_enc, self._character_set)
        possible_words = self._word_dictionary[self._get_key_for_word(processed_word)]
        cipher_copy = cipher.copy()

        # Determine what to fill cipher with
        # Replace this cipher with a negation of the already known values
        # Those values cannot become the result of the cipher anymore
        if len(cipher.values()) <= 0:
            cipher_fill = '.'
        else:
            cipher_fill = '[^' + ''.join(cipher.values()) + ']'

        # Fill cipher with missing keys
        for c in list(self._character_set):
            if c not in cipher_copy.keys():
                cipher_copy[c] = cipher_fill

        regex_string = decipher_text(processed_word, cipher_copy)

        regex = re.compile(regex_string)

        # Filter out possibilities with current cipher keys
        possible_words = list(filter(regex.search, possible_words))
        return possible_words

    def generate_possible_words(self, word_enc, cipher={}):
        processed_word = process_word(word_enc, self._character_set)
        possible_words = self.get_possible_words(processed_word, cipher)

        for word_dec in possible_words:
            cipher_for_this = create_cipher(processed_word, word_dec)
            yield word_dec, {**cipher_for_this, **cipher}
