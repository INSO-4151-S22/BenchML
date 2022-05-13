from config.celery import celery
from controller.modules.benchmarking.optimize import Optimize
from controller.modules.benchmarking.attack import Attack
import json
import config


@celery.task(track_started=True)
def optimize_model(url, model_type):
    resources = json.loads(config.get_settings().optimizer_resources)
    return Optimize(resources=resources, model_type=model_type).run(url)


@celery.task(track_started=True)
def adversarial_attack_model(url, model_type):
    resources = json.loads(config.get_settings().optimizer_resources)
    return Attack(resources=resources, model_type=model_type).run(url)
