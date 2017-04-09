import string
import pickle
import re
import glob
import os
import argparse
import sys
from collections import Counter
from subprocess import call

from code.translator import decipher_text, create_cipher
from code.decipher.functions import process_word

# Cache for valid_word_lists
loaded_valid_word_lists = {}

character_set_global = string.ascii_lowercase


def prepare_wordlist(language, character_set):
    """
    Prepare downloading, loading and processing of the wordlist

    :param language: Language to be used
    :param character_set: character set to be used
    :return:
    """
    # Find correct data directory
    correct_data_path = None
    for path in ('data', '../data'):
        if os.path.isdir(path):
            correct_data_path = path

    pickle_file_name = "{}wiktionary.p".format(language)

    matches_pickle = list(glob.glob("{0}/{1}".format(correct_data_path, pickle_file_name)))

    if len(matches_pickle) > 0:
        # There is a pickle file already, load that one
        return pickle.load(open(matches_pickle[0], "rb"))

    else:
        matches = list(glob.glob("{0}/{1}wiktionary*".format(correct_data_path, language)))

        if len(matches) <= 0:
            # No match, try to download file
            call(["/decipher_capstone/data/download_wordlist.sh", str(language),
                  str("/decipher_capstone/data")])
            matches = list(glob.glob("{0}/{1}wiktionary*".format(correct_data_path, language)))

            # If still not there, raise error
            if len(matches) <= 0:
                raise FileNotFoundError("No file for this language")

        with open(matches[0]) as f:
            file_lines = f.readlines()

        valid_word_list = set()
        for entry in file_lines[1:]:
            try:
                if re.split(r'\t+', entry.strip())[0] == '0':
                    valid_word = re.split(r'\t+', entry.strip())[1]
                    processed_word = process_word(valid_word, character_set)
                    if processed_word is not None:
                        valid_word_list.add(processed_word)

            except IndexError:
                # Issue parsing this line, ignore it
                pass

        # Write to pickle file
        pickle.dump(valid_word_list, open(correct_data_path + "/" + pickle_file_name, "wb"))
        return valid_word_list


def get_valid_word_list(language, character_set):
    """
    Load the word list for a specific language.

    :param character_set: character set to be used for word list
    :param language: language to get words for
    :return: list of words valid in language
    """
    if language in loaded_valid_word_lists.keys():
        # Already loaded in memory
        valid_word_list = loaded_valid_word_lists[language]
    else:
        valid_word_list = prepare_wordlist(language, character_set)
        # Add to memory
        loaded_valid_word_lists[language] = valid_word_list

    return valid_word_list


class PossibilityGenerator(object):
    _character_set = character_set_global
    _word_dictionary = None

    def __init__(self, character_set, language):
        """
        Get the character frequency for a given language
        """
        self._character_set = character_set

        # if language not in ['en', 'nl']:
        #     raise NotImplementedError(
        #         'Language {} not supported'.format(language))

        self._load_language_words(language)

    def _load_language_words(self, language):
        # Load the words of the language and process them into a dict
        words = get_valid_word_list(language=language, character_set=self._character_set)

        self._word_dictionary = dict()
        for word in words:
            try:
                self._word_dictionary[self._get_key_for_word(word)].append(word)
            except KeyError:
                self._word_dictionary[self._get_key_for_word(word)] = [word]

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

if __name__ == '__main__':
    # Parse the arguments given
    parser = argparse.ArgumentParser(description='Pre load wordlist')
    parser.add_argument("-l", "--language", help="Specify Language to prepare", type=str)
    args = parser.parse_args()

    # Check if any of them are not given
    if args.language is None:
        print('Not all arguments for script given')
        print(parser.print_help())
        sys.exit(1)

    print("--- Preload the wordlist for language: {} ---".format(args.language))
    prepare_wordlist(language=args.language, character_set=character_set_global)
