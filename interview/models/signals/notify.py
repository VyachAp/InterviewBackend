from django.db.models.signals import post_save
from django.dispatch import receiver
from interview.models import Post, NotifyUser


def notify_user(sender, instance, **kwargs):
    status = instance.status
    if status == 'Decline':
        NotifyUser.objects.create(user_id=instance.author,
                                  notify_text=f'Вам отказано в публикации поста {instance.title}. Причина: {instance.additional_info}')
    if status == 'Published':
        NotifyUser.objects.create(user_id=instance.author,
                                  notify_text=f'Ваш пост {instance.title} успешно опубликован.')
    if status == 'Moderation':
        NotifyUser.objects.create(user_id=instance.author,
                                  notify_text=f'Ваш пост {instance.title} взят на рассмотрение модератором.')


post_save.connect(notify_user, sender=Post, dispatch_uid='notify_user')
