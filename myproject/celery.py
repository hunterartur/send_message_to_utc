from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем Django настройки по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Создаем экземпляр Celery
app = Celery('myproject')

# Загружаем настройки из конфигурации Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в приложениях
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
