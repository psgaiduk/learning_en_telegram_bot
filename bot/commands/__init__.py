from commands.check_answer_time import (
    handle_check_answer_time,
    handle_check_answer_time_other_data,
)
from commands.registration import handle_registration
from commands.wait_name import (
    handle_wait_name,
    handle_wait_name_incorrect_work,
    handle_wait_name_incorrect_work_buttons,
)
from commands.wait_en_level import (
    handle_wait_en_level,
    handle_wait_en_level_incorrect_text,
)
from commands.update_profile import (
    handle_update_profile,
    handle_update_profile_name,
    handle_update_profile_en_level,
    handle_update_profile_close,
    handle_update_profile_other_data,
)
from commands.check_words import (
    handle_check_words_after_learn_words,
    handle_check_words_after_read,
    handle_check_word_click_known,
    handle_check_words_other_data,
)
from commands.read_sentence import (
    handle_read_sentence,
    handle_read_sentence_after_learn_words,
    handle_read_sentence_other_data,
    handle_end_read_sentence_today,
    handle_end_read_sentence_today_after_learn_words,
)
from commands.learn_words import handle_error_learn_words, handle_learn_words
from commands.start_lean_words import (
    handle_error_start_learn_words,
    handle_start_lean_words,
)
