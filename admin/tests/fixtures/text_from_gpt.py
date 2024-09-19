from pytest import fixture


@fixture
def text_from_gpt() -> str:
    text = (
        "Let's go see the birds. --- "
        "Пойдем посмотрим на птиц. --- "
        "let || давай || part || лет [lɛt]; go || идти || v || гоу [ɡoʊ]; see || смотреть || v || си [siː]; --- "
        "Present Simple"
    )
    return text


@fixture
def words_from_text(text_from_gpt) -> str:
    return text_from_gpt.split(" --- ")[2]
