from fastapi import Depends, HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload

from api.v1.history import version_1_history_router
from database import get_db
from dto.models import HistoryBookSentenceModelDTO, HistoryWordModelDTO
from dto.requests import CreateBooksSentencesDTO, UpdateHistoryBooksSentencesDTO
from dto.responses import OneResponseDTO
from models import (
    BooksSentences,
    Users,
    UsersBooksSentencesHistory,
    UsersWordsHistory,
    Words,
    sentence_word_association,
)


async def get_sentence_history_dto(sentence_info: dict) -> HistoryBookSentenceModelDTO:
    """Get history book sentence dto."""

    sentence_info["id"] = sentence_info["id"]
    sentence_info["book_id"] = sentence_info["sentence"].book_id
    sentence_info["telegram_id"] = sentence_info["telegram_user_id"]
    sentence_info["sentence_id"] = sentence_info["sentence_id"]
    sentence_info["is_read"] = sentence_info["is_read"]
    sentence_info["created_at"] = sentence_info["created_at"]

    words = []
    for word in sentence_info["words"]:
        word = word.__dict__
        word_info = {}
        words_history = {}
        if word["users_words_history"]:
            words_history = word["users_words_history"][0].__dict__

        word_info["id"] = words_history.get("id")
        word_info["word_id"] = word["word_id"]
        word_info["word"] = word["word"]
        word_info["type_word_id"] = word["type_word_id"]
        word_info["translation"] = word["translation"]
        word_info["is_known"] = words_history.get("is_known")
        word_info["count_view"] = words_history.get("count_view")
        word_info["correct_answers"] = words_history.get("correct_answers")
        word_info["incorrect_answers"] = words_history.get("incorrect_answers")
        word_info["correct_answers_in_row"] = words_history.get("correct_answers_in_row")
        word_info["created_at"] = words_history.get("created_at")
        word_info["updated_at"] = words_history.get("updated_at")

        words.append(HistoryWordModelDTO(**word_info))

    sentence_info["words"] = words

    return HistoryBookSentenceModelDTO(**sentence_info)


@version_1_history_router.post(
    path="/sentences/",
    response_model=OneResponseDTO[HistoryBookSentenceModelDTO],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Telegram user or sentence not found."},
        status.HTTP_400_BAD_REQUEST: {"description": "User already know word."},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_history_sentences_for_telegram_id(
    request: CreateBooksSentencesDTO, db: Session = Depends(get_db)
) -> OneResponseDTO:
    """Create history sentence for telegram user."""

    telegram_id = request.telegram_id
    sentence_id = request.sentence_id

    telegram_user = db.query(Users).filter(Users.telegram_id == telegram_id).first()
    if not telegram_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    sentence = db.query(BooksSentences).filter(BooksSentences.sentence_id == sentence_id).first()
    if not sentence:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sentence not found.")

    old_history_sentence = (
        db.query(UsersBooksSentencesHistory)
        .filter(
            UsersBooksSentencesHistory.telegram_user_id == telegram_id,
            UsersBooksSentencesHistory.sentence_id == sentence_id,
        )
        .first()
    )

    if old_history_sentence:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already study this sentence.",
        )

    new_history_sentence = UsersBooksSentencesHistory(
        telegram_user_id=telegram_id,
        sentence_id=sentence_id,
    )
    db.add(new_history_sentence)
    db.commit()

    history_sentence = (
        db.query(UsersBooksSentencesHistory)
        .join(
            BooksSentences,
            BooksSentences.sentence_id == UsersBooksSentencesHistory.sentence_id,
        )
        .options(joinedload(UsersBooksSentencesHistory.sentence))
        .filter(UsersBooksSentencesHistory.id == new_history_sentence.id)
        .first()
    )

    if history_sentence:
        words_with_history = (
            db.query(Words)
            .join(
                sentence_word_association,
                sentence_word_association.c.wordsmodel_id == Words.word_id,
            )
            .outerjoin(
                UsersWordsHistory,
                and_(
                    UsersWordsHistory.word_id == Words.word_id,
                    UsersWordsHistory.telegram_user_id == telegram_id,
                ),
            )
            .options(joinedload(Words.users_words_history))
            .filter(sentence_word_association.c.bookssentencesmodel_id == history_sentence.sentence_id)
            .all()
        )
        history_sentence.words = words_with_history

    history_word_dto = await get_sentence_history_dto(history_sentence.__dict__)

    return OneResponseDTO(detail=history_word_dto)


@version_1_history_router.patch(
    path="/sentences/{history_book_sentence_id}/",
    response_model=OneResponseDTO,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Telegram user or sentence or history sentence not found."},
        status.HTTP_400_BAD_REQUEST: {"description": "Is read or check words required."},
    },
    status_code=status.HTTP_200_OK,
)
async def update_history_sentences_for_telegram_id(
    history_book_sentence_id: int,
    request: UpdateHistoryBooksSentencesDTO,
    db: Session = Depends(get_db),
) -> OneResponseDTO:
    """Update history sentence for telegram user."""

    is_read = request.is_read
    check_words = request.check_words

    history_book_sentence = (
        db.query(UsersBooksSentencesHistory).filter(UsersBooksSentencesHistory.id == history_book_sentence_id).first()
    )
    if not history_book_sentence:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History sentence not found.")

    if is_read is None and check_words is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Is read or check words required.",
        )

    if check_words is not None:
        history_book_sentence.check_words = check_words
    if is_read is not None:
        history_book_sentence.is_read = request.is_read
    db.commit()

    return OneResponseDTO(detail="Success.")
