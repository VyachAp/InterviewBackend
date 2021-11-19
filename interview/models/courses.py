from django.db import models
from .profession import Profession


class Course(models.Model):
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)
    link = models.URLField("Ссылка", null=True, blank=True)

    class Meta:
        app_label = "interview"
        verbose_name = "Ссылка на курс"
        verbose_name_plural = "Ссылки на курсы"
        db_table = "courses"

    def __str__(self):
        return f"Profession: {self.profession.name} - {self.link}"
