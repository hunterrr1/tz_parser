from celery import Celery

celery = Celery('parser', broker='redis://redis:6379/0', broker_connection_retry_on_startup=True)
