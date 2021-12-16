from django.db import models


class Scope(models.Model):
    """Модель для сфер деятельности"""

    name = models.CharField("Название", max_length=128)
    has_professions = models.BooleanField("Имеет профессии", default=True)
    has_questions = models.BooleanField("Имеет вопросы", default=True)

    class Meta:
        app_label = "interview"
        verbose_name = "Сфера деятельности"
        verbose_name_plural = "Сферы деятельности"
        db_table = "scopes"

    def __str__(self):
        return "Scope: " + self.name


class SubScope(models.Model):
    """Модель для подраздела сферы деятельности"""

    name = models.CharField("Название", max_length=64)
    scope = models.ForeignKey(Scope, on_delete=models.PROTECT)
    icon = models.CharField("Название иконки", max_length=32, null=True)

    class Meta:
        app_label = "interview"
        verbose_name = "Подраздел сферы"
        verbose_name_plural = "Подразделы сферы"
        db_table = "subscope"

    def __str__(self):
        return f"SubScope: {self.scope.name} - {self.name}"
