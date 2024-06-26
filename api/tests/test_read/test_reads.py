from datetime import datetime

from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import BooksModel, Users, UsersBooksHistory, UsersBooksSentencesHistory, BooksSentences
from settings import settings
from tests.fixtures import *
from tests.connect_db import db_session


@mark.usefixtures('create_test_database', 'telegram_users_mock', 'book_mock', 'book_sentences_mock', 'words_mock')
class TestReadApi:

    def setup_method(self):
        self._headers = {'X-API-Key': settings.api_key}
        self._client = TestClient(app)
        self._url = '/api/v1/read'

    def test_get_first_sentence_for_not_read_early(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            assert users_history_book is None
            users_history_book_sentence = (
                db.query(UsersBooksSentencesHistory)
                .filter(UsersBooksSentencesHistory.telegram_user_id == telegram_id)
                .first()
            )
            assert users_history_book_sentence is None

        url = f'{self._url}/{telegram_id}/'
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()['detail']

        with db_session() as db:
            users_history_book = db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            assert users_history_book is not None
            book_id = users_history_book.book_id
            assert users_history_book.start_read is not None
            assert users_history_book.end_read is None
            users_history_book_sentence = (
                db.query(UsersBooksSentencesHistory)
                .filter(UsersBooksSentencesHistory.telegram_user_id == telegram_id)
                .first()
            )
            assert users_history_book_sentence is not None
            assert users_history_book_sentence.id == response['history_sentence_id']
            assert users_history_book_sentence.is_read is False
            assert users_history_book_sentence.sentence_id == response['sentence_id']
            assert users_history_book_sentence.telegram_user_id == telegram_id
            book = db.query(BooksModel).filter(BooksModel.book_id == book_id).first()
            assert f'{book.author} - {book.title}' in response['text']
            assert len(response['words']) <= 5
            sentence = db.query(BooksSentences).filter(BooksSentences.sentence_id == response['sentence_id']).first()
            assert sentence.order == 1

    def test_get_first_sentence_for_next_read_book(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            assert users_history_book is None
            old_book = db.query(BooksModel).filter(
                BooksModel.level_en_id == telegram_user.level_en_id,
                BooksModel.title == 'First Book - Part 1',
            ).first()
            old_book_id = old_book.book_id
            history_book = UsersBooksHistory(
                telegram_user_id=telegram_id,
                book_id=old_book.book_id,
                start_read=datetime.utcnow(),
                end_read=datetime.utcnow(),
            )
            db.add(history_book)
            db.commit()

        url = f'{self._url}/{telegram_id}/'
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()['detail']

        with db_session() as db:
            assert old_book_id != response['book_id']
            users_history_book = db.query(UsersBooksHistory).filter(
                UsersBooksHistory.telegram_user_id == telegram_id,
                UsersBooksHistory.book_id == response['book_id'],
            ).first()
            assert users_history_book is not None
            book_id = users_history_book.book_id
            assert users_history_book.start_read is not None
            assert users_history_book.end_read is None
            users_history_book_sentence = (
                db.query(UsersBooksSentencesHistory)
                .filter(
                    UsersBooksSentencesHistory.telegram_user_id == telegram_id,
                    UsersBooksSentencesHistory.sentence_id == response['sentence_id'],
                )
                .first()
            )
            assert users_history_book_sentence is not None
            assert users_history_book_sentence.is_read is False
            assert users_history_book_sentence.sentence_id == response['sentence_id']
            assert users_history_book_sentence.telegram_user_id == telegram_id
            book = db.query(BooksModel).filter(BooksModel.book_id == book_id).first()
            assert f'{book.author} - {book.title}' in response['text']
            assert len(response['words']) <= 5
            sentence = db.query(BooksSentences).filter(BooksSentences.sentence_id == response['sentence_id']).first()
            assert sentence.order == 1
            assert users_history_book_sentence.id == response['history_sentence_id']
            assert '- part 2' in response['text'].lower()

    def test_get_first_sentence_for_random_read_book(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            assert users_history_book is None
            old_book = db.query(BooksModel).filter(
                BooksModel.level_en_id == telegram_user.level_en_id,
                BooksModel.title == 'Second Book',
            ).first()
            old_book_id = old_book.book_id
            history_book = UsersBooksHistory(
                telegram_user_id=telegram_id,
                book_id=old_book.book_id,
                start_read=datetime.utcnow(),
                end_read=datetime.utcnow(),
            )
            db.add(history_book)
            db.commit()

        url = f'{self._url}/{telegram_id}/'
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()['detail']

        with db_session() as db:
            assert old_book_id != response['book_id']
            users_history_book = db.query(UsersBooksHistory).filter(
                UsersBooksHistory.telegram_user_id == telegram_id,
                UsersBooksHistory.book_id == response['book_id'],
            ).first()
            assert users_history_book is not None
            book_id = users_history_book.book_id
            assert users_history_book.start_read is not None
            assert users_history_book.end_read is None
            users_history_book_sentence = (
                db.query(UsersBooksSentencesHistory)
                .filter(
                    UsersBooksSentencesHistory.telegram_user_id == telegram_id,
                    UsersBooksSentencesHistory.sentence_id == response['sentence_id'],
                )
                .first()
            )
            assert users_history_book_sentence is not None
            assert users_history_book_sentence.is_read is False
            assert users_history_book_sentence.sentence_id == response['sentence_id']
            assert users_history_book_sentence.telegram_user_id == telegram_id
            book = db.query(BooksModel).filter(BooksModel.book_id == book_id).first()
            assert f'{book.author} - {book.title}' in response['text']
            assert len(response['words']) <= 5
            sentence = db.query(BooksSentences).filter(BooksSentences.sentence_id == response['sentence_id']).first()
            assert sentence.order == 1
            assert users_history_book_sentence.id == response['history_sentence_id']
            assert '- part 2' not in response['text'].lower()

    def test_get_first_sentence_after_last_sentence(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            assert users_history_book is None
            old_book = db.query(BooksModel).filter(BooksModel.level_en_id == telegram_user.level_en_id).first()
            old_book_id = old_book.book_id
            history_book = UsersBooksHistory(
                telegram_user_id=telegram_id,
                book_id=old_book.book_id,
                start_read=datetime.utcnow(),
            )
            db.add(history_book)
            last_sentence = (
                db.query(BooksSentences)
                .filter(BooksSentences.book_id == old_book_id)
                .order_by(BooksSentences.order.desc())
                .first()
            )
            history_book_sentence = UsersBooksSentencesHistory(
                telegram_user_id=telegram_id,
                sentence_id=last_sentence.sentence_id,
                is_read=True,
            )
            db.add(history_book_sentence)
            db.commit()

        url = f'{self._url}/{telegram_id}/'
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()['detail']

        with db_session() as db:
            assert old_book_id != response['book_id']
            users_history_book = db.query(UsersBooksHistory).filter(
                UsersBooksHistory.telegram_user_id == telegram_id,
                UsersBooksHistory.book_id == response['book_id'],
            ).first()
            assert users_history_book is not None
            book_id = users_history_book.book_id
            assert users_history_book.start_read is not None
            assert users_history_book.end_read is None
            users_history_book_sentence = (
                db.query(UsersBooksSentencesHistory)
                .filter(
                    UsersBooksSentencesHistory.telegram_user_id == telegram_id,
                    UsersBooksSentencesHistory.sentence_id == response['sentence_id'],
                )
                .first()
            )
            assert users_history_book_sentence is not None
            assert users_history_book_sentence.is_read is False
            assert users_history_book_sentence.sentence_id == response['sentence_id']
            assert users_history_book_sentence.telegram_user_id == telegram_id
            assert users_history_book_sentence.id == response['history_sentence_id']
            book = db.query(BooksModel).filter(BooksModel.book_id == book_id).first()
            assert f'{book.author} - {book.title}' in response['text']
            assert len(response['words']) <= 5
            sentence = db.query(BooksSentences).filter(BooksSentences.sentence_id == response['sentence_id']).first()
            assert sentence.order == 1

            old_book_history = db.query(UsersBooksHistory).filter(
                UsersBooksHistory.telegram_user_id == telegram_id,
                UsersBooksHistory.book_id == old_book_id,
            ).first()
            assert old_book_history is not None
            assert old_book_history.end_read is not None

    def test_get_next_sentence_from_book(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            assert users_history_book is None
            old_book = db.query(BooksModel).filter(BooksModel.level_en_id == telegram_user.level_en_id).first()
            old_book_id = old_book.book_id
            history_book = UsersBooksHistory(
                telegram_user_id=telegram_id,
                book_id=old_book.book_id,
                start_read=datetime.utcnow(),
            )
            db.add(history_book)
            first_sentence = (
                db.query(BooksSentences)
                .filter(BooksSentences.book_id == old_book_id)
                .order_by(BooksSentences.order.asc())
                .first()
            )
            history_book_sentence = UsersBooksSentencesHistory(
                telegram_user_id=telegram_id,
                sentence_id=first_sentence.sentence_id,
                is_read=True,
            )
            db.add(history_book_sentence)
            db.commit()

        url = f'{self._url}/{telegram_id}/'
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()['detail']

        with db_session() as db:
            assert old_book_id == response['book_id']
            users_history_book = db.query(UsersBooksHistory).filter(
                UsersBooksHistory.telegram_user_id == telegram_id,
                UsersBooksHistory.book_id == response['book_id'],
            ).first()
            assert users_history_book is not None
            assert users_history_book.start_read is not None
            assert users_history_book.end_read is None
            users_history_book_sentence = (
                db.query(UsersBooksSentencesHistory)
                .filter(
                    UsersBooksSentencesHistory.telegram_user_id == telegram_id,
                    UsersBooksSentencesHistory.sentence_id == response['sentence_id'],
                )
                .first()
            )
            assert users_history_book_sentence is not None
            assert users_history_book_sentence.is_read is False
            assert users_history_book_sentence.sentence_id == response['sentence_id']
            assert users_history_book_sentence.telegram_user_id == telegram_id
            assert users_history_book_sentence.id == response['history_sentence_id']
            assert len(response['words']) <= 5
            sentence = db.query(BooksSentences).filter(BooksSentences.sentence_id == response['sentence_id']).first()
            assert sentence.order == 2

            old_book_history = db.query(UsersBooksHistory).filter(
                UsersBooksHistory.telegram_user_id == telegram_id,
                UsersBooksHistory.book_id == old_book_id,
            ).first()
            assert old_book_history is not None
            assert old_book_history.end_read is None

    @mark.parametrize('count_sentences, expected_status', [
        (1, status.HTTP_200_OK), (4, status.HTTP_200_OK), (5, status.HTTP_206_PARTIAL_CONTENT), (10, status.HTTP_206_PARTIAL_CONTENT)])
    def test_more_history_sentences(self, count_sentences, expected_status):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            assert users_history_book is None
            old_book = db.query(BooksModel).filter(BooksModel.level_en_id == telegram_user.level_en_id).first()
            old_book_id = old_book.book_id
            history_book = UsersBooksHistory(
                telegram_user_id=telegram_id,
                book_id=old_book.book_id,
                start_read=datetime.utcnow(),
            )
            db.add(history_book)
            for _ in range(count_sentences):
                sentence = (
                    db.query(BooksSentences)
                    .filter(BooksSentences.book_id == old_book_id)
                    .order_by(BooksSentences.order.asc())
                    .first()
                )
                history_book_sentence = UsersBooksSentencesHistory(
                    telegram_user_id=telegram_id,
                    sentence_id=sentence.sentence_id,
                    is_read=True,
                )
                db.add(history_book_sentence)
                db.commit()

        url = f'{self._url}/{telegram_id}/'
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == expected_status

    def test_get_same_sentence_if_not_read_sentence(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            assert users_history_book is None
            old_book = db.query(BooksModel).filter(BooksModel.level_en_id == telegram_user.level_en_id).first()
            old_book_id = old_book.book_id
            history_book = UsersBooksHistory(
                telegram_user_id=telegram_id,
                book_id=old_book.book_id,
                start_read=datetime.utcnow(),
            )
            db.add(history_book)
            first_sentence = (
                db.query(BooksSentences)
                .filter(BooksSentences.book_id == old_book_id)
                .order_by(BooksSentences.order.asc())
                .first()
            )
            first_sentence_id = first_sentence.sentence_id
            history_book_sentence = UsersBooksSentencesHistory(
                telegram_user_id=telegram_id,
                sentence_id=first_sentence_id,
                is_read=False,
                check_words=[],
            )
            db.add(history_book_sentence)
            db.commit()

        url = f'{self._url}/{telegram_id}/'
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()['detail']

        with db_session() as db:
            assert old_book_id == response['book_id']
            assert first_sentence_id == response['sentence_id']
            users_history_book = db.query(UsersBooksHistory).filter(
                UsersBooksHistory.telegram_user_id == telegram_id,
                UsersBooksHistory.book_id == response['book_id'],
            ).first()
            assert users_history_book is not None
            assert users_history_book.start_read is not None
            assert users_history_book.end_read is None
            users_history_book_sentence = (
                db.query(UsersBooksSentencesHistory)
                .filter(
                    UsersBooksSentencesHistory.telegram_user_id == telegram_id,
                    UsersBooksSentencesHistory.sentence_id == response['sentence_id'],
                )
                .first()
            )
            assert users_history_book_sentence is not None
            assert users_history_book_sentence.is_read is False
            assert users_history_book_sentence.sentence_id == response['sentence_id']
            assert users_history_book_sentence.telegram_user_id == telegram_id
            assert users_history_book_sentence.id == response['history_sentence_id']
            assert len(response['words']) <= 5

    def test_not_get_read_without_headers(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id

        url = f'{self._url}/{telegram_id}/'
        response = self._client.get(url=url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_get_read_with_wrong_api_key_headers(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id

        url = f'{self._url}/{telegram_id}/'
        response = self._client.get(url=url, headers={'X-API-Key': 'test'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
