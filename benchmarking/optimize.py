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

    def create_model_from_args(self, config):
        # Model type for now only supports keras and pytorch
        if config['model_type'] == 'keras':
            return self.create_model_keras()
        elif config['model_type'] == 'pytorch':
            return self.create_model_pytorch(config)
        else: 
            return None

    def create_model_keras(self, config):
        '''
        Creates a keras model based on given structure with the usage of config values in hyperparameters.
        '''
        return None
    
    def create_model_pytorch(self, config):
        '''
        Creates a pytorch model based on given structure with the usage of config values in hyperparameters.
        '''
        class Net(nn.Module):
            
            def __init__(self, layers, config):
                super().__init__()
                # Define layers based on init Args
                self.model = []
                for layer in layers:
                    if layer[0] == "Conv2d":
                        # Extract parameters for Conv2D layer 
                        layer_args = []
                        for i in range(1, len(layer)):
                            if isinstance(layer[i], str) and config[layer[i]]:
                                layer_args.append(config[layer[i]])  # Applies a config value to it if available
                            else:
                                layer_args.append(layer[i])
                        self.model.append(nn.Conv2d(*layer_args))  # Creates a Conv2D layer with the appropiate parameters
                    elif layer[0] == "MaxPool2d":
                        # Extract parameters for MaxPool2D layer 
                        layer_args = []
                        for i in range(1, len(layer)):
                            if isinstance(layer[i], str) and config[layer[i]]:
                                layer_args.append(config[layer[i]])  # Applies a config value to it if available
                            else:
                                layer_args.append(layer[i])
                        self.model.append(nn.MaxPool2d(*layer_args))  # Creates a MaxPool2D layer with the appropiate parameters
                    elif layer[0] == "Linear":
                        # Extract parameters for Linear layer 
                        layer_args = []
                        for i in range(1, len(layer)):
                            if isinstance(layer[i], str) and config[layer[i]]:
                                layer_args.append(config[layer[i]])  # Applies a config value to it if available
                            else:
                                layer_args.append(layer[i])
                        self.model.append(nn.Linear(*layer_args))  # Creates a linear layer with the appropiate parameters
                    elif layer[0] == "view":
                        view_args = ["view"]
                        for i in range(1, len(layer)):
                            view_args.append(layer[i])
                        self.model.append(view_args)
                    elif layer[0] == "relu":
                        self.model.append(nn.ReLU)
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

            def to_string(self):
                string = ""
                i = 0
                for fun in self.model:
                    if isinstance(fun, list) and fun[0] == "view":
                        string += "Layer {}: x.view(".format(i)
                        for index in range(1, len(fun)):
                            string += " {} ".format(fun[index])
                        string += ")\n"
                    elif isinstance(fun, type):
                        string += "Layer {}: {}\n".format(i, fun.__name__)
                    else:
                        string += "Layer {}: {}\n".format(i, fun._get_name)
                    i+=1
                return string

        return Net(config["layers"], config)

    def train_cifar(self, config):
        net = Optimize.create_model_from_args(self, config)
        return net

    def data_loader(self):
        pass


    
    
    
