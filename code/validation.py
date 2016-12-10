import re
import glob

loaded_valid_word_lists = {}


def get_valid_word_list(language):
    """
    Load the word list for a specific language.

    :param data_path: Path to the data folder
    :param language: language to get words for
    :return: list of words valid in language
    """
    if language in loaded_valid_word_lists.keys():
        return loaded_valid_word_lists[language]
    else:
        matches = list()
        for data_path in ('data', '../data'):
            filepart_to_search = data_path+"/{}wiktionary".format(language)
            matches += list(glob.glob(filepart_to_search + '*'))

        if len(matches) <= 0:
            # No match, try to download file
            raise FileNotFoundError("No file for this language")
        else:
            dict_file = matches[0]

        with open(dict_file) as f:
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

        loaded_valid_word_lists[language] = valid_word_list
        return valid_word_list


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
