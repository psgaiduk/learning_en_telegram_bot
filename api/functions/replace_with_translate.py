from re import IGNORECASE, escape, sub


def replace_with_translation(text: str, words: list) -> str:
    """
    Replace words with translation.

    :param text: Test for replace.
    :param words: Words for replace.
    :return: New text with translation.
    """
    words = sorted(words, key=lambda w: len(w.word), reverse=True)
    replaced_ranges = []

    for word_info in words:
        word_text = word_info.word.lower()
        word_translation = word_info.translation['ru']

        def replace_func(match):
            original_word = match.group(0)
            match_range = match.span()

            for replaced_range in replaced_ranges:
                if replaced_range[0] <= match_range[0] and replaced_range[1] >= match_range[1]:
                    return original_word

            replaced_ranges.append(match_range)
            return f'<b>{original_word}</b> ({word_translation})'

        text = sub(fr'\b{escape(word_text)}\b', replace_func, text, flags=IGNORECASE)
    return text
