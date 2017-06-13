import string
import logging

from code.decipher.functions import get_encoded_words_from_msg
from code.decipher.possibility_generator import PossibilityGenerator


class Solver(object):
    language = None
    _pg = None
    _character_set = None

    def __init__(self, language, character_set=string.ascii_lowercase, logger=logging.getLogger()):
        """
        Setup the solver by initializing a possibility generator.
        
        :param language: Language to be used
        :param character_set: Character set
        :param logger: Logger
        """
        self.logger = logger
        self.logger.info('Initialise solver for language: {}'.format(language))

        self.language = language
        self._character_set = character_set
        self._pg = PossibilityGenerator(character_set=character_set, language=language)

    def _calc_complexity(self, word_list, cipher={}):
        """
        Calculate the complexity for a list of words.
        
        :param word_list: word list
        :param cipher: cipher used so far
        :return: complexity score
        """
        complexity = 1
        for w in word_list:
            complexity *= len(self._pg.get_possible_words(w, cipher))

        return complexity

    def _get_best_cipher_and_words_correct(self, ordered_list_words_enc, cipher_so_far={}):
        """
        Recursively walk through the list of words, looping through the possibilities for each of them and keeping
        track of the total amount of correctly translated words. The cipher with the best_score (most words found) 
        will be returned.
        
        :param ordered_list_words_enc: List of encoded words, ordered on the number of possible decodings for each 
        :param cipher_so_far: Cipher found so far
        :return: Best cipher to be used based on this set of encoded words
        """
        if len(ordered_list_words_enc) <= 0:
            return cipher_so_far, 0
        else:
            best_cipher = None
            best_score = 0
            for possible_word_dec, cipher_used in self._pg.generate_possible_words(
                    ordered_list_words_enc[0], cipher_so_far):
                new_cipher_so_far, num_correct = self._get_best_cipher_and_words_correct(
                    ordered_list_words_enc[1:], cipher_used)
                if num_correct + 1 > best_score:
                    best_cipher = new_cipher_so_far
                    best_score = num_correct + 1

            if best_score <= 0:
                # We didn't find anything, ignore this word from now on
                return self._get_best_cipher_and_words_correct(ordered_list_words_enc[1:],
                                                               cipher_so_far)
            else:
                return best_cipher, best_score

    def _generate_subset_words_per_letter(self, word_list, cipher_fixed, max_complexity=1e11,
                                          min_set_size=4):
        """
        Determine the best order to walk through the letters (certain ones will be easier to workout as they have fewer
        possible decodings).
        Now we choose the letters that occur in most words first.
        
        The maximum complexity determines how big the search space can be (fewer words means lower complexity).
        The minimum set size determines the minimum amount of words we want to have in a set, otherwise we won't start
        decoding.
        These parameters allow control over the accuracy vs speed of the algorithm.
        
        :param word_list: Complete word list of encoded words
        :param cipher_fixed: Cipher so far
        :param max_complexity: Maximum complexity to start decoding a set of words for a letter
        :param min_set_size: Minimum set of words to be used when decoding
        :return: generator that yields characters to be decoded with a list of words to use for that.
        """
        letter_scores = list()
        for char in list(self._character_set):
            word_set = [w for w in word_list if char in w]
            if len(word_set) == 0:
                avg_word_set_complexity = 0
            else:
                avg_word_set_complexity = min([self._calc_complexity([w], {}) for w in word_set])
            score = len(word_set) - avg_word_set_complexity
            letter_scores.append((char, score, word_set))

        letter_scores = sorted(letter_scores, key=lambda x: x[1], reverse=True)

        for char, char_score, word_set in letter_scores:
            complexity = self._calc_complexity(word_set, cipher_fixed)

            # As long as the complexity is too high, reduce the set size
            while complexity > max_complexity and len(word_set) >= min_set_size:
                word_set = word_set[:-1]
                complexity = self._calc_complexity(word_set, cipher_fixed)

            # We only take sets of minimum x words
            if len(word_set) >= min_set_size:
                yield char, word_set

    def solve(self, msg_enc, max_complexity=1e11, min_set_size=10):
        """
        Decode the encode message.

        :param min_set_size: Minimum size a set of words should be to decipher a letter
        :param msg_enc: The encoded message
        :param max_complexity: Maximum complexity used in searching, reducing this will speed up
        the program but make it less accurate
        :return: Decoded message
        """
        word_enc_possibility_dict = dict()

        for word_enc in get_encoded_words_from_msg(msg_enc=msg_enc,
                                                   character_set=self._character_set):
            word_enc_possibility_dict[word_enc] = self._pg.get_possible_words(word_enc)

        # Check if words are already in correct language
        already_correct = 0
        for key, values in word_enc_possibility_dict.items():
            if key in values:
                already_correct += 1

        if already_correct / len(word_enc_possibility_dict.keys()) > 0.8:
            # No translation needed
            return {c: c for c in self._character_set}, already_correct / len(word_enc_possibility_dict.keys())

        # Sort the word_encoded list based on possibilities
        word_enc_list_ordered = sorted(word_enc_possibility_dict,
                                       key=lambda k: len(word_enc_possibility_dict[k]),
                                       reverse=False)

        correct_word_count = 0
        total_word_count = 0

        cipher_already_fix = {}
        while min_set_size > 0:
            self.logger.debug("---- Start deciphering with minimum set of {}".format(min_set_size))

            gen_subsets = self._generate_subset_words_per_letter(word_enc_list_ordered,
                                                                 cipher_already_fix,
                                                                 max_complexity=max_complexity,
                                                                 min_set_size=min_set_size)
            for used_letter, used_set in gen_subsets:
                if used_letter not in cipher_already_fix.keys():
                    self.logger.debug("\t-- Letter {}".format(used_letter))
                    found_cipher, correct_words = self._get_best_cipher_and_words_correct(used_set,
                                                                                          cipher_already_fix)
                    correctly_translated = correct_words / len(used_set)
                    correct_word_count += correct_words
                    total_word_count += len(used_set)

                    try:
                        if found_cipher[used_letter] in cipher_already_fix.values():
                            self.logger.debug(
                                "\t\t!!!! PROBLEM: this letter ({}) has been used to translate to already".format(
                                    found_cipher[used_letter]))
                        else:
                            cipher_already_fix[used_letter] = found_cipher[used_letter]

                            self.logger.debug("\t\tDecided for {0}:{1}".format(used_letter,
                                                                   found_cipher[used_letter]))
                            self.logger.debug("\t\tNumber of correctly translated words: {0}/{1} ({2}%)".format(
                                correct_words, len(used_set), int(100 * correctly_translated)))
                    except KeyError:
                        self.logger.debug(
                            "\t\tWe'd hoped to find this one, but couldnt: {}".format(used_letter))

            min_set_size -= 1

        self.logger.debug("Number of keys found: {}".format(len(cipher_already_fix)))
        try:
            perc_correct = correct_word_count / total_word_count
        except:
            perc_correct = 0
        self.logger.info("Correctly translated for language {}: {}".format(self.language, perc_correct))
        return cipher_already_fix, perc_correct
