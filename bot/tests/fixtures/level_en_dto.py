from pytest import fixture

from dto import LevelEnDTOModel


@fixture
def level_en():
    return LevelEnDTOModel(
        id=1,
        title='Beginner',
        description='Beginner description',
        order=1,
    )
