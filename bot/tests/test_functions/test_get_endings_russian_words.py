from functions import get_end_of_russian_word_func


def test_get_end_of_russian_word_func():
    endings = ["конец", "конца", "концов"]

    assert get_end_of_russian_word_func(1, endings) == "конец"  # 1
    assert get_end_of_russian_word_func(21, endings) == "конец"  # 21
    assert get_end_of_russian_word_func(101, endings) == "конец"  # 101

    assert get_end_of_russian_word_func(2, endings) == "конца"  # 2
    assert get_end_of_russian_word_func(3, endings) == "конца"  # 3
    assert get_end_of_russian_word_func(4, endings) == "конца"  # 4
    assert get_end_of_russian_word_func(22, endings) == "конца"  # 22
    assert get_end_of_russian_word_func(23, endings) == "конца"  # 23
    assert get_end_of_russian_word_func(24, endings) == "конца"  # 24

    assert get_end_of_russian_word_func(5, endings) == "концов"  # 5
    assert get_end_of_russian_word_func(11, endings) == "концов"  # 11
    assert get_end_of_russian_word_func(12, endings) == "концов"  # 12
    assert get_end_of_russian_word_func(13, endings) == "концов"  # 13
    assert get_end_of_russian_word_func(14, endings) == "концов"  # 14
    assert get_end_of_russian_word_func(15, endings) == "концов"  # 15
    assert get_end_of_russian_word_func(100, endings) == "концов"  # 100
    assert get_end_of_russian_word_func(111, endings) == "концов"  # 111
    assert get_end_of_russian_word_func(115, endings) == "концов"  # 115

    assert get_end_of_russian_word_func(1, ["конец"]) == ""  # Меньше 3 окончаний
    assert get_end_of_russian_word_func(1, ["конец", "конца"]) == ""  # Меньше 3 окончаний
