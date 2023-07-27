from django.db.models import BigIntegerField, CharField, IntegerField, Model


class HeroLevelsModel(Model):
    title = CharField(max_length=64)
    need_experience = BigIntegerField()
    count_sentences = IntegerField()
    count_games = IntegerField()
    order = IntegerField()

    class Meta:
        db_table = 'hero_levels'
        ordering = ['order']
