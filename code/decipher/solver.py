import string

from code.decipher.functions import get_encoded_words_from_msg
from code.decipher.possibility_generator import PossibilityGenerator


class Solver(object):
    _pg = None
    _character_set = None

    def __init__(self, language, character_set=string.ascii_lowercase):
        self._character_set = character_set
        self._pg = PossibilityGenerator(character_set=character_set, language=language)

    def _calc_complexity(self, word_list, cipher={}):
        complexity = 1
        for w in word_list:
            complexity *= len(self._pg.get_possible_words(w, cipher))

        return complexity

    def _get_best_cipher_and_words_correct(self, ordered_list_words_enc, cipher_so_far={}):
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
        # Determine the best order to walk through the letters (certain onces will be easier to workout)
        # Now we choose the letters that occur in most words first
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

    def solve(self, msg_enc):
        word_enc_possibility_dict = dict()

        for word_enc in get_encoded_words_from_msg(msg_enc=msg_enc,
                                                   character_set=self._character_set):
            possibilities = self._pg.get_possible_words(word_enc)
            word_enc_possibility_dict[word_enc] = possibilities

        # Sort the word_encoded list based on possibilities
        word_enc_list_ordered = sorted(word_enc_possibility_dict,
                                       key=lambda k: len(word_enc_possibility_dict[k]),
                                       reverse=False)

        cipher_already_fix = {}
        min_set_size = 10
        while min_set_size > 0:
            print("---- Start deciphering with minimum set of {}".format(min_set_size))

            gen_subsets = self._generate_subset_words_per_letter(word_enc_list_ordered,
                                                                 cipher_already_fix,
                                                                 max_complexity=1e12,
                                                                 min_set_size=min_set_size)
            for used_letter, used_set in gen_subsets:
                if used_letter not in cipher_already_fix.keys():
                    print("\t-- Letter {}".format(used_letter))
                    found_cipher, correct_words = self._get_best_cipher_and_words_correct(used_set,
                                                                                          cipher_already_fix)
                    correctly_translated = correct_words / len(used_set)

                    try:
                        if found_cipher[used_letter] in cipher_already_fix.values():
                            print(
                                "\t\t!!!! PROBLEM: this letter ({}) has been used to translate to already".format(
                                    found_cipher[used_letter]))
                        else:
                            cipher_already_fix[used_letter] = found_cipher[used_letter]

                            print("\t\tDecided for {0}:{1}".format(used_letter,
                                                                   found_cipher[used_letter]))
                            print("\t\tNumber of correctly translated words: {0}/{1} ({2}%)".format(
                                correct_words, len(used_set), int(100 * correctly_translated)))
                    except KeyError:
                        print(
                            "\t\tWe'd hoped to find this one, but couldnt: {}".format(used_letter))

            min_set_size -= 1

        print()
        print("Number of keys found: {}".format(len(cipher_already_fix)))
        return cipher_already_fix
