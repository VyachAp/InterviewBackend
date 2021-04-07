from django.db import models


class Questions(models.Model):
    """Модель для вопросов"""

    question = models.TextField("Текст вопроса")
    answer = models.TextField("Текст ответа")
    subscope = models.ForeignKey(
        "interview.SubScope",
        related_name="questions",
        on_delete=models.PROTECT,
        verbose_name="Подраздел",
    )

    class Meta:
        app_label = "interview"
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        db_table = "questions"

    def __str__(self):
        return f"Question {self.pk}: {self.question}"
