from django.db import models


class Profession(models.Model):
    """Модель для профессий"""

    name = models.CharField("Название", max_length=128)
    english_name = models.CharField("Название на английском", max_length=128, null=True, blank=True)
    scope = models.ForeignKey("interview.Scope", on_delete=models.PROTECT)
    description = models.TextField("Описание")
    image_url = models.URLField(null=True, blank=True)

    class Meta:
        app_label = "interview"
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"
        db_table = "professions"

    def __str__(self):
        return f"Profession: {self.scope.name} - {self.name}"


class ProfessionSalaries(models.Model):
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)
    parse_date = models.DateField(verbose_name="Дата сбора информации", auto_now_add=True)
    low_salary = models.IntegerField("Нижняя вилка", null=True)
    high_salary = models.IntegerField("Верхняя вилка", null=True)
    region = models.CharField("Регион", choices=[('1', 'Москва'), ('113', 'Россия')], max_length=64)

    class Meta:
        app_label = "interview"
        verbose_name = "Зарплата профессии"
        verbose_name_plural = "Зарплаты профессий"
        db_table = "professions_salaries"

    def __str__(self):
        return f"Profession: {self.profession.name} - {self.parse_date} - {self.region}"


class ProfessionLinks(models.Model):
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)
    courses = models.URLField("Курсы", null=True, blank=True)
    vacancies = models.URLField("Вакансии", null=True, blank=True)

    class Meta:
        app_label = "interview"
        verbose_name = "Ссылки профессии"
        verbose_name_plural = "Ссылки профессий"
        db_table = "professions_links"

    def __str__(self):
        return f"Profession: {self.profession.name} - {self.courses} - {self.vacancies}"
