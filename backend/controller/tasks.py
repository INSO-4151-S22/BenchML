from config import celery
from controller.modules.benchmarking.optimize import Optimize


@celery.task(track_started=True)
def optimize_model(url):
    return Optimize().run(url)
