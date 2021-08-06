from django.db import models


class NotifyUser(models.Model):
    notify_text = models.TextField("Комментарий")
    is_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    user = models.ForeignKey('interview.Account', on_delete=models.CASCADE)

    class Meta:
        app_label = "interview"
        verbose_name = "Уведомление пользователя"
        verbose_name_plural = "Уведомления пользователя"
        db_table = "user_notifications"

    def __str__(self):
        return f"Notification: {self.pk} - {self.user_id}"
