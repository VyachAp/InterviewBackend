from django.db import models


class Profession(models.Model):
    """Модель для профессий"""

    name = models.CharField("Название", max_length=128)
    subscope = models.CharField("Подкатегория сферы деятельности", max_length=128)
    description = models.TextField("Описание")

    class Meta:
        app_label = "interview"
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"
        db_table = "professions"

    def __str__(self):
        return "Profession: " + self.name
