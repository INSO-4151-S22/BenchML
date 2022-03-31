from celery import Celery
from backend.controller.modules.benchmarking.optimize import Optimize


celery = Celery(
    __name__,
    broker="",
    backend="",
    worker_redirect_stdouts=False
)


@celery.task(track_started=True)
def optimize_model(url):
    return Optimize().run(url)
