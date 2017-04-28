import re


def process_word(original_word, character_set):
    """
    Process a word by taking out any invalid characters.
    
    :param original_word: word to process
    :param character_set: valid characters
    :return: processed word
    """
    processed_word = original_word.lower()

    # Check if letters in character_set
    valid_word = True
    for letter in list(processed_word):
        if letter not in character_set:
            valid_word = False

    if valid_word:
        return processed_word
    else:
        return None


def get_encoded_words_from_msg(msg_enc, character_set):
    """
    From a message, get the encoded words by splitting up the sentence and process the word.
    
    :param msg_enc: Encoded message
    :param character_set: Character set to use
    :return: list of words from message
    """
    word_enc_list = set()

    # Run through each unique encoded word and process it accordingly
    for word_enc in set(re.findall(r"[\w']+", msg_enc)):
        processed_word = process_word(word_enc, character_set)
        if processed_word is not None:
            word_enc_list.add(processed_word)

    return word_enc_list
