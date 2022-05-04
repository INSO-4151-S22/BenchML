from config.celery import celery
from controller.modules.benchmarking.optimize import Optimize


@celery.task(track_started=True)
def optimize_model(url, model_type):
    return Optimize({'cpu': 2, 'gpu':0}, model_type).run(url)
