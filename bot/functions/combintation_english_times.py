from itertools import combinations


def get_combinations(count_combinations: int) -> list[str]:
    """
    Get combinations of english times.

    :param count_combinations:
    :return: list of combinations
    """
    all_english_times = [
        "Present Simple",
        "Past Simple",
        "Future Simple",
        "Present Continuous",
        "Past Continuous",
        "Present Perfect",
        "Past Perfect",
        "Future Perfect",
        "Present Perfect Continuous",
        "Past Perfect Continuous",
        "Future Perfect Continuous",
    ]

    combinations_list = []
    for comb in combinations(all_english_times, count_combinations):
        combinations_list.append(", ".join(comb))
    return combinations_list
