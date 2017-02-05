import re
import glob
import pickle
import os

loaded_valid_word_lists = {}


def get_valid_word_list(language):
    """
    Load the word list for a specific language.

    :param language: language to get words for
    :return: list of words valid in language
    """
    if language in loaded_valid_word_lists.keys():
        # Already loaded in memory
        valid_word_list = loaded_valid_word_lists[language]
    else:
        # Find correct data directory
        correct_data_path = None
        for path in ('data', '../data'):
            if os.path.isdir(path):
                correct_data_path = path

        pickle_file_name = "{}wiktionary.p".format(language)

        matches_pickle = list(glob.glob("{0}/{1}".format(correct_data_path, pickle_file_name)))

        if len(matches_pickle) > 0:
            # There is a pickle file already, load that one
            valid_word_list = pickle.load(open(matches_pickle[0], "rb"))

        else:
            matches = list(glob.glob("{0}/{1}wiktionary*".format(correct_data_path, language)))

            if len(matches) <= 0:
                # No match, try to download file
                raise FileNotFoundError("No file for this language")

            with open(matches[0]) as f:
                file_lines = f.readlines()

            valid_word_list = set()
            for entry in file_lines[1:]:
                try:
                    if re.split(r'\t+', entry.strip())[0] == '0':
                        valid_word = re.split(r'\t+', entry.strip())[1]
                        valid_word_list.add(valid_word)
                except IndexError:
                    # Issue parsing this line, ignore it
                    pass

            # Write to pickle file
            pickle.dump(valid_word_list, open(correct_data_path + "/" + pickle_file_name, "wb"))

        # Add to memory
        loaded_valid_word_lists[language] = valid_word_list

    return valid_word_list


def check_valid_word_perc(wordlist, language):
    """
    Check the percentage of valid words in the wordlist given the language.

    :param wordlist: List of words to check for existence
    :param language: Language of the words
    :return: Percentage of valid words
    """
    if len(wordlist) <= 0:
        return 0.0

    valid_word_count = 0
    valid_words = get_valid_word_list(language)

    for word in wordlist:
        if word in valid_words:
            valid_word_count += 1

    valid_word_perc = float(valid_word_count) / len(wordlist)
    return valid_word_perc


def is_valid_sentence(sentence, language, acceptance_perc=0.8):
    """
    Check if a sentence is valid in a certain language.

    :param sentence: sentence to check
    :param language: language to check sentence against
    :param acceptance_perc: percentage of words that need to be correct
    :return: True if valid words exceed acceptance percentage
    """
    if sentence == "":
        return False

    # Remove all characters but words and lowercase all
    processed_sentence = " ".join(re.findall("[a-zA-Z]+", sentence.lower()))

    # Extract a list of words and check the percentage correct
    wordlist = processed_sentence.split(" ")
    valid_word_perc = check_valid_word_perc(wordlist, language)

    return valid_word_perc >= acceptance_perc
