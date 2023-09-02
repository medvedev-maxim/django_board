from django.db.models.signals import post_save, post_delete, post_migrate
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import Reply, Post
from django.conf import settings


@receiver(post_save, sender=Reply)
def notify_add_reply (sender, instance, **kwargs):
    send_mail( 
        subject=f'{instance.feedbackUser} оставил отклик на объявление "{instance.feedbackPost.title}"',
        message=f'"{instance.text}"\n\nОбработайте этот отклик и проверьте другие в разделе http://127.0.0.1:8000/replys/',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.feedbackPost.user.email]
    )

@receiver(post_delete, sender=Reply)
def notify_delete_reply (sender, instance, **kwargs):
    send_mail( 
        subject=f'Ваш отклик на "{instance.feedbackPost.title}" ОТКЛОНЕН!',
        message=f'Ваш отклик "{instance.text}" был ОТКЛОНЕН и УДАЛЕН!\nПопробуйте предложенить другой вариант по адресу http://127.0.0.1:8000/posts/{instance.feedbackPost.id}/',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.feedbackUser.email]
    ) 

@receiver(post_migrate, sender=Reply)
def notify_apply_reply (sender, instance, **kwargs):
    send_mail( 
        subject=f'Ваш отклик на "{instance.feedbackPost.title}" ОДОБРЕН!',
        message=f'Ваш отклик "{instance.text}" был ОДОБРЕН!\nСвяжитесь с автором объявления по адресу {instance.feedbackPost.user.email}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.feedbackUser.email]
    ) 