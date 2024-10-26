from pytest import fixture


@fixture
def api_get_user_stats():
    return {"count_of_words": 0, "count_of_new_words": 0, "time_to_next_word": 0}
