from enum import Enum


class State(Enum):
    """States for FSM."""

    new_client = "NEW_CLIENT"
    wait_name = "WAIT_NAME"
    wait_en_level = "WAIT_EN_LEVEL"
    read_book = "READ_BOOK"
    read_book_end = "READ_BOOK_END"
    check_words = "CHECK_WORDS"
    grammar = "GRAMMAR"
    update_profile = "UPDATE_PROFILE"
    check_answer_time = "CHECK_ANSWER_TIME"
    registration = "REGISTRATION"
    error = "ERROR"
    records = "RECORDS"
    achievements = "ACHIEVEMENTS"
    start_learn_words = "START_LEARN_WORDS"
    learn_words = "LEARN_WORDS"
