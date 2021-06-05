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


class SuggestedQuestions(models.Model):
    """Модель для предложенных вопросов"""

    question = models.TextField("Текст вопроса")
    answer = models.TextField("Текст ответа")
    scope = models.CharField("Сфера деятельности", max_length=256)
    subscope = models.CharField("Подраздел сферы деятельности", max_length=256)
    user = models.ForeignKey('interview.Account', related_name='Вопросы', on_delete=models.PROTECT)

    class Meta:
        app_label = "interview"
        verbose_name = "Предложенный вопрос"
        verbose_name_plural = "Предложенные вопросы"
        db_table = "suggested_questions"

    def __str__(self):
        return f"Question {self.pk}: {self.question}"
