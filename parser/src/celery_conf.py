from celery_app import celery
from datetime import timedelta
import main

celery.conf.task_routes = {
             'celery_coins.get_data': {'queue': 'celery'},
        }

celery.conf.beat_schedule = {
        'get_data': {
            'task': 'main.get_data',
            'schedule': timedelta(seconds=60)
        }
    }