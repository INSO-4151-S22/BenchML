from argparse import ArgumentTypeError
import ray
from ray import tune
import numpy as np
from ray.tune.schedulers import ASHAScheduler
import requests
import json
from backend.controller.modules.benchmarking.keras_optimizer import KerasOptimizer
from backend.controller.modules.benchmarking.pytorch_optimizer import PyTorchOptimizer

class Optimize:

    def __init__(self, resources = {'cpu': 2, 'gpu':1}):
        self.resources = resources

    def create_model_from_args(self, config):
        """Based on the model type in config, create a model for use with ray tune."""
        if config['model_type'] == 'keras':
            return KerasOptimizer().create_model(config)
        elif config['model_type'] == 'pytorch':
            return PyTorchOptimizer().create_model(config)
        else: 
            raise Exception(f"No model type available for {config['model_type']}")

    def train(self, config):
        '''
        Trains a model for each iteration in `tune.run`. 
        Reports back to the hyperparameter optimizer the results from each iteration.

        Args:
            config: A JSON object containing the model arguments.
        '''

        net = Optimize.create_model_from_args(self, config)
        loss, accuracy = net.train()       

        # Report findings to ray for hyperparameter tuning/optimization
        tune.report(loss=loss, accuracy=accuracy)
        print("Training completed for model")

    def run(self, url):
        """Run optimizer.

            Obtains configuration for model from user input url. Runs the Hyperparameter
            optimizer `tune.run` with the training function for the model_type to obtain
            the best trial.

            Args: 
                url: User-input for config.json used in model creation. 
            
            Returns:
                A JSON object with the best trial architecture and metrics. 
        """
        config = self.get_model_config(url)
        scheduler = ASHAScheduler(
                max_t=10,
                grace_period=1,
                reduction_factor=2
            )
        
        result = tune.run(
            tune.with_parameters(self.train),
            resources_per_trial={"cpu": self.resources['cpu'], "gpu": self.resources['gpu']}, # For Google Colab Environment
            config=config,
            metric="mean_accuracy",
            mode="max",
            num_samples=10,
            scheduler=scheduler,
            stop={"mean_accuracy": 0.99}
        )

        best_trial = result.get_best_trial("loss", "min", "last")
        res = {'best_trial_config': str(best_trial.config), 'validation_loss': str(best_trial.last_result["loss"]), 'validation_accuracy': str(best_trial.last_result["accuracy"])}
        return res

    def get_model_config(self, url):
        """Gets model configuration from user-input url.
        
            Requests the json file from the url and parses it to convert it into a programmable json.
            This json is then used for model creation.

            Args:
                url: User-input for config.json used in model creation.

            Returns:
                Dictionary object that contains the configuration of the model to be created.
        """
        config = json.loads(requests.get(url).text)
        parsed_config = {}

        for k in config.keys():
            if k == "layers":
                parsed_config[k] = []
                for layer in config[k]:
                    l = []
                    for param in layer:
                        if(isinstance(param, str)):
                            try:
                                l.append(int(param))
                            except ValueError:
                                l.append(param)
                    parsed_config[k].append(l)
            else:
                parsed_config[k] = config[k]
        
        learning_rate = tune.loguniform(1e-4, 1e-1)
        batch_size = tune.choice([2, 4, 8, 16])

        for k in parsed_config.keys():
            if k == 'model_type' or k == 'layers':
                pass
            elif k == 'lr' and parsed_config[k] and len(parsed_config[k]) == 0:
                parsed_config[k] = learning_rate
            elif k == 'batch_size' and parsed_config[k] and len(parsed_config[k]) == 0:
                parsed_config[k] = batch_size
            else:
                parsed_config[k] = tune.sample_from(lambda _: 2 ** np.random.randint(2, 9))
                
        return parsed_config


    
    
    
