from argparse import ArgumentTypeError
import ray
from ray import tune
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import random_split
import torchvision
import torchvision.transforms as transforms

class Optimize:

    def __init__(self):
        pass

    def create_model_from_args(self, model_type, layers, config):
        # Model type for now only supports keras and pytorch
        if model_type == 'keras':
            return self.create_model_keras()
        elif model_type == 'pytorch':
            return self.create_model_pytorch()
        else: 
            return None

    def create_model_keras(self, model_type, layers, config):
        '''
        Creates a keras model based on given structure with the usage of config values in hyperparameters.
        '''
        return None
    
    def create_model_pytorch(self, layers, config):
        '''
        Creates a pytorch model based on given structure with the usage of config values in hyperparameters.
        '''
        class Net(nn.Module):
            
            def __init__(self, layers, config):
                super().__init__()
                # Define layers based on init Args
                self.model = []
                for layer in layers:
                    if layer[0] == "Conv2D":
                        # Extract parameters for Conv2D layer 
                        layer_args = []
                        for i in range(1, len(layer)):
                            if config[layer[i]]:
                                layer_args.append(config[layer[i]])  # Applies a config value to it if available
                            else:
                                layer_args.append(layer[i])
                        self.model.append(nn.Conv2D(*layer_args))  # Creates a Conv2D layer with the appropiate parameters
                    elif layer[0] == "MaxPool2D":
                        # Extract parameters for MaxPool2D layer 
                        layer_args = []
                        for i in range(1, len(layer)):
                            if config[layer[i]]:
                                layer_args.append(config[layer[i]])  # Applies a config value to it if available
                            else:
                                layer_args.append(layer[i])
                        self.model.append(nn.MaxPool2D(*layer_args))  # Creates a MaxPool2D layer with the appropiate parameters
                    elif layer[0] == "Linear":
                        # Extract parameters for Linear layer 
                        layer_args = []
                        for i in range(1, len(layer)):
                            if config[layer[i]]:
                                layer_args.append(config[layer[i]])  # Applies a config value to it if available
                            else:
                                layer_args.append(layer[i])
                        self.model.append(nn.Linear(*layer_args))  # Creates a linear layer with the appropiate parameters
                    elif layer[0] == "view":
                        view_args = ["view"]
                        for i in range(1, len(layer)):
                            view_args.append(layer[i])
                        self.model.append(view_args)
                    else:
                        raise ArgumentTypeError("The layer {} is incompatible with the optimization model creation for this current version.".format(layer[0]))

            def forward(self, x):
                # Define forward function based on init args 
                for fun in self.model:
                    if fun[0] == "view":
                        x = x.view(*fun[1])  # Gets the args for that function to apply it to the view/reshape method
                    else:
                        x = fun(x)
                return x

        return Net(layers, config)

    def train_cifar(self, config):
        pass

    def data_loader(self):
        pass

    
    
