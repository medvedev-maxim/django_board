import logging
 
from django.conf import settings
from ...models import Post, User
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.conf import settings
 
 
logger = logging.getLogger(__name__)
 
 
# наша задача по выводу текста на экран
def my_job():
    date_filter = datetime.now() - timedelta(weeks=1)
    post_list = Post.objects.filter(dateCreation__gt=date_filter)
    user_list = User.objects.all()
    # print(date_filter)
    template = 'mail/sendnewposts_comm.html'

    for u in user_list:
        if u.email:

            html = render_to_string(
            template_name=template,
                context = {
                    'post': post_list,
                },
            )

            msg = EmailMultiAlternatives(
                subject='Список новых объявлений за последнюю неделю',
                body='',
                from_email= settings.DEFAULT_FROM_EMAIL,
                to=[u.email]
            )

            msg.attach_alternative(html, 'text/html')
            msg.send()   



 
# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            # trigger=CronTrigger(second="*/5"),  # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),             
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")