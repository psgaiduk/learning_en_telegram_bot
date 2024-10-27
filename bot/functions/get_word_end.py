def get_end_of_russian_word_func(number: int, endings: list) -> str:
    """Create end of russian words.

    Args:
        number (int): number.
        endings (list): endings for numbers [1, 2, 100]

    Returns:
        str: end of word
    """
    if len(endings) < 3:
        return ""
    if number % 10 == 1 and number % 100 != 11:
        return endings[0]
    if 2 <= number % 10 <= 4 and not (12 <= number % 100 <= 14):
        return endings[1]

    return endings[2]
