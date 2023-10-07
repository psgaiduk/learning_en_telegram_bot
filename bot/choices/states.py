from enum import StrEnum


class State(StrEnum):
    """States for FSM."""

    new_client = 'NEW_CLIENT'
    wait_name = 'WAIT_NAME'
    wait_en_level = 'WAIT_EN_LEVEL'
    read_book = 'READ_BOOK'
    check_words = 'CHECK_WORDS'
    grammar = 'GRAMMAR'
    update_profile = 'UPDATE_PROFILE'
    registration = 'REGISTRATION'
    error = 'ERROR'
    records = 'RECORDS'
