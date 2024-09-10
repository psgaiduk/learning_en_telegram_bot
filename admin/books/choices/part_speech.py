from app.choices import AdminChoiceEnum


class PartOfSpeechChoice(AdminChoiceEnum):
    """Part of speech."""

    noun = ("n", "Существительное")
    adjective = ("adj", "Прилагательное")
    verb = ("v", "Глагол")
    adverb = ("adv", "Наречие")
    preposition = ("pre", "Предлог")
    pronoun = ("pro", "Местоимение")
    conjunction = ("c", "Союз")
    particle = ("part", "Частица")
    interjection = ("i", "Междометие")
