from django.db import models


class Feedback(models.Model):
    details = models.TextField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        app_label = "interview"
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратные связи"

    def __str__(self):
        return f'{self.id} - {self.date}'
