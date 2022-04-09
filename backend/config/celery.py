from celery import Celery
import config


celery = Celery(
    __name__,
    broker=config.get_settings().celery_broker_url,
    backend=config.get_settings().celery_backend_url,
    worker_redirect_stdouts=False
)
