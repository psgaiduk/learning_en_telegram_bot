from enum import Enum


class PartOfSpeechChoice(Enum):
    """Part of speech."""

    n = "Существительное"
    adj = "Прилагательное"
    v = "Глагол"
    adv = "Наречие"
    pre = "Предлог"
    pro = "Местоимение"
    c = "Союз"
    part = "Частица"
    i = "Междометие"
    num = "Числительное"
