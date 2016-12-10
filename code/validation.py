import re
import requests


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

    for word in wordlist:
        query_string = "https://{0}.wiktionary.org/w/api.php" \
                       "?action=query&titles={1}&format=json".format(language, word)
        response = requests.get(query_string)

        try:
            print(response.json())
            if '-1' not in response.json()['query']['pages'].keys():
                valid_word_count += 1
        except ValueError:
            print("{0} couldn't be translated. (language: {1})".format(word, language))

    valid_word_perc = float(valid_word_count) / len(wordlist)
    return valid_word_perc
