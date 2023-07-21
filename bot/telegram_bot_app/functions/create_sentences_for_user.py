from db.models import Users


async def create_sentences_for_user(
        sentences: list[str],
        translate_sentences: list[str],
        user: Users,
) -> list[tuple[str, str]]:
    """
    Function for create sentences for user.
    :param sentences: List of sentences on learn language.
    :param translate_sentences: List of sentences on main language.
    :param user: user from database.
    :return: list of sentences for user.
    """
    sentences_for_user = []

    max_length = {
        0: 40,
        1: 80,
        2: 120,
        3: 180,
    }

    sentence_on_main_language = ''
    sentence_on_learn_language = ''
    for index, sentence in enumerate(sentences):
        sentence_translate = translate_sentences[index]
        if not sentence_on_learn_language:
            sentence_on_learn_language = sentence.strip()
            sentence_on_main_language = sentence_translate.strip()
        elif len(sentence_on_learn_language + sentence) > max_length.get(user.level, 120):
            sentences_for_user.append((sentence_on_learn_language, sentence_on_main_language))
            sentence_on_main_language = ''
            sentence_on_learn_language = ''
        else:
            sentence_on_learn_language = ' '.join((sentence_on_learn_language, sentence.strip()))
            sentence_on_main_language = ' '.join((sentence_on_main_language, sentence_translate.strip()))

    if sentence_on_learn_language:
        sentences_for_user.append((sentence_on_learn_language, sentence_on_main_language))

    return sentences_for_user
