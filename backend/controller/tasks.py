from config.celery import celery
from controller.modules.benchmarking.optimize import Optimize
import json
import config


@celery.task(track_started=True)
def optimize_model(url, model_type):
    resources = json.loads(config.get_settings().optimizer_resources)
    return Optimize(resources, model_type).run(url)
