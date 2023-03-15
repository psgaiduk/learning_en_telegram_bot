from constants import Constant


async def create_sentences_for_user(sentences: list[str], translate_sentences: list[str]) -> list[tuple[str, str]]:
    """
    Function for create sentences for user.
    :param sentences: List of sentences on learn language.
    :param translate_sentences: List of sentences on main language.
    :return: list of sentences for user.
    """
    sentences_for_user = []

    sentence_on_main_language = ''
    sentence_on_learn_language = ''
    for index, sentence in enumerate(sentences):
        sentence_translate = translate_sentences[index]
        if not sentence_on_learn_language:
            sentence_on_learn_language = sentence.strip()
            sentence_on_main_language = sentence_translate.strip()
        elif len(sentence_on_learn_language + sentence) > Constant.max_length_sentence_for_user.value:
            sentences_for_user.append((sentence_on_learn_language, sentence_on_main_language))
            sentence_on_main_language = ''
            sentence_on_learn_language = ''
        else:
            sentence_on_learn_language = ' '.join((sentence_on_learn_language, sentence.strip()))
            sentence_on_main_language = ' '.join((sentence_on_main_language, sentence_translate.strip()))

    if sentence_on_learn_language:
        sentences_for_user.append((sentence_on_learn_language, sentence_on_main_language))

    return sentences_for_user
