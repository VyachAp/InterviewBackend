from django.db import models
from django.core.exceptions import ValidationError
from django.apps import apps


class Post(models.Model):
    statuses = [
        ("Created", "Создан"),
        ("Moderation", "На модерации"),
        ("Published", "Опубликован"),
        ("Declined", "Отказано в публикации")
    ]
    title = models.CharField(verbose_name="Заголовок", max_length=256, null=True, blank=True)
    status = models.CharField(verbose_name="Статус", choices=statuses, default="Created", max_length=32)
    additional_info = models.TextField("Информация от администратора/модератора", null=True, blank=True)
    body = models.TextField(verbose_name="Текст поста")
    date_created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    author = models.ForeignKey('interview.Account', on_delete=models.PROTECT, related_name='posts')

    def save(self, **kwargs):
        self.clean()
        # TODO: Debug to signals
        saved = super(Post, self).save(**kwargs)
        notify_cls = apps.get_model('interview.NotifyUser')
        if self.status == 'Decline':
            notify_cls.objects.create(user=self.author,
                                      notify_text=f'Вам отказано в публикации поста {self.title}. Причина: {self.additional_info}')
        if self.status == 'Published':
            notify_cls.objects.create(user=self.author,
                                      notify_text=f'Ваш пост {self.title} успешно опубликован.')
        if self.status == 'Moderation':
            notify_cls.objects.create(user=self.author,
                                      notify_text=f'Ваш пост {self.title} взят на рассмотрение модератором.')
        return saved

    def clean(self):
        super(Post, self).clean()
        if self.status == 'Declined' and not self.additional_info:
            raise ValidationError('Опишите причину отказа', code='not_described')

    class Meta:
        app_label = "interview"
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        db_table = "posts"

    def __str__(self):
        return f"Post: {self.pk} - {self.title}"


class PostLikes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('interview.Account', on_delete=models.CASCADE)

    class Meta:
        app_label = "interview"
        verbose_name = "Лайк поста"
        verbose_name_plural = "Лайки поста"
        db_table = "post_likes"

        unique_together = ('post_id', 'user_id')

    def __str__(self):
        return f"Post - LikedBy: {self.post_id} - {self.user}"


class PostComments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField("Комментарий")
    date_created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    user = models.ForeignKey('interview.Account', on_delete=models.CASCADE)

    class Meta:
        app_label = "interview"
        verbose_name = "Комментарий поста"
        verbose_name_plural = "Комментарии поста"
        db_table = "post_comments"

    def __str__(self):
        return f"Post - CommentedBy: {self.post_id} - {self.user}"
