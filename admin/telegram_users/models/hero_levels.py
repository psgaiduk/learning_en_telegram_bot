from django.db.models import BigIntegerField, CharField, IntegerField, Model


class HeroLevelsModel(Model):
    title = CharField(max_length=64)
    need_experience = BigIntegerField()
    count_sentences = IntegerField()
    count_games = IntegerField()
    order = IntegerField()

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = "Hero level"
        verbose_name_plural = "Hero levels"
        db_table = "hero_levels"
        ordering = ["order"]
