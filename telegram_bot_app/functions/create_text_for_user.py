from re import findall


def create_text_for_user(current_sentence: list, next_sentences: list) -> str:
    pattern = r'\*(.*?)\*'
    sentence_on_learn_language = current_sentence[0]
    hard_words_learn_language = findall(pattern, sentence_on_learn_language)
    sentence_on_main_language = current_sentence[1]
    hard_words_main_language = findall(pattern, sentence_on_main_language)

    hard_words_with_translate = []
    for word_index, hard_word in enumerate(hard_words_learn_language):
        hard_word_insert = f'\n{hard_word} - {hard_words_main_language[word_index]}'
        hard_words_with_translate.append(hard_word_insert)

    return '\n'.join(
        [
            sentence_on_learn_language,
            f'{"".join(hard_words_with_translate)}'
            '\n<u>Посмотреть перевод:</u>',
            f'<tg-spoiler>{sentence_on_main_language}</tg-spoiler>',
            f'\nДо конца осталось: {len(next_sentences)} шт.'
        ])