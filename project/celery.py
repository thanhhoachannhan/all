import os, time
from celery import Celery, shared_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@shared_task
def task_one():
    time.sleep(10)
    print('Hello World')
    return 'Hello World'
