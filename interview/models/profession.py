from django.db import models


class Profession(models.Model):
    """Модель для профессий"""

    name = models.CharField("Название", max_length=128)
    english_name = models.CharField("Название на английском", max_length=128, null=True, blank=True)
    scope = models.ForeignKey("interview.Scope", on_delete=models.PROTECT)
    description = models.TextField("Описание")

    class Meta:
        app_label = "interview"
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"
        db_table = "professions"

    def __str__(self):
        return f"Profession: {self.scope.name} - {self.name}"
