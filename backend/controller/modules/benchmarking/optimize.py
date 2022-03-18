from argparse import ArgumentTypeError
import ray
from ray import tune
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import random_split
import torchvision
import torch.optim as optim
import torchvision.transforms as transforms
from filelock import FileLock
import numpy as np
import os
from ray.tune.schedulers import ASHAScheduler
import requests
import json

class Optimize:

    def __init__(self):
        pass

    def create_model_from_args(self, config):
        """Based on the model type in config, create a model for use with ray tune."""
        if config['model_type'] == 'keras':
            return self.create_model_keras(config)
        elif config['model_type'] == 'pytorch':
            return self.create_model_pytorch(config)
        else: 
            return None

    def create_model_keras(self, config):
        """Creates a keras model based on given structure with the usage of config values in hyperparameters.

           TODO!!
        """
        # TODO
        return None
    
    def create_model_pytorch(self, config):
        """Creates a pytorch model based on given structure with the usage of config values in hyperparameters.

           Takes in a model configuration and creates a Net object that contains the nn.Module objects to run a 
           Pytorch neural network. 

           Args:
                config: configuration values that contain model architecture.

            Returns:
                Pytorch Neural Network with provided configuration architecture.

            Raises:
                ArgumentTypeError: An invalid pytorch layer was found in config.
        """
        class Reshape(nn.Module):
            '''
            Reshape layer to be used for replacing x.view and add it as a ModuleList.
            '''
            def __init__(self, *args):
                super(Reshape, self).__init__()
                self.shape = args

            def forward(self, x):
                return x.view(self.shape)

        class Net(nn.Module):
            
            def __init__(self, layers, config):
                super().__init__()
                # Define layers based on init Args
                self.model = nn.ModuleList()
                for layer in layers:
                    print(layer[0])
                    if layer[0] == 'Conv2d':
                        # Extract parameters for Conv2D layer 
                        layer_args = []
                        for i in range(1, len(layer)):
                            if isinstance(layer[i], str) and config[layer[i]]:
                                layer_args.append(config[layer[i]])  # Applies a config value to it if available
                            else:
                                layer_args.append(layer[i])
                        self.model.append(nn.Conv2d(*layer_args))  # Creates a Conv2D layer with the appropiate parameters
                    elif layer[0] == 'MaxPool2d':
                        # Extract parameters for MaxPool2D layer 
                        layer_args = []
                        for i in range(1, len(layer)):
                            if isinstance(layer[i], str) and config[layer[i]]:
                                layer_args.append(config[layer[i]])  # Applies a config value to it if available
                            else:
                                layer_args.append(layer[i])
                        self.model.append(nn.MaxPool2d(*layer_args))  # Creates a MaxPool2D layer with the appropiate parameters
                    elif layer[0] == 'Linear':
                        # Extract parameters for Linear layer 
                        layer_args = []
                        for i in range(1, len(layer)):
                            if isinstance(layer[i], str) and config[layer[i]]:
                                layer_args.append(config[layer[i]])  # Applies a config value to it if available
                            else:
                                layer_args.append(layer[i])
                        self.model.append(nn.Linear(*layer_args))  # Creates a linear layer with the appropiate parameters
                    elif layer[0] == 'Reshape':
                        # Extract parameters for Conv2D layer 
                        layer_args = []
                        for i in range(1, len(layer)):
                            if isinstance(layer[i], str) and config[layer[i]]:
                                layer_args.append(config[layer[i]])  # Applies a config value to it if available
                            else:
                                layer_args.append(layer[i])
                        self.model.append(Reshape(*layer_args))  # Creates a Reshape layer with the appropiate parameters
                    elif layer[0] == 'ReLU':
                        self.model.append(nn.ReLU())
                    else:
                        raise ArgumentTypeError("The layer {} is incompatible with the optimization model creation for this current version.".format(layer[0]))

            def forward(self, x):
                # Define forward function based on init args 
                for fun in self.model:
                    x = fun(x)
                return x

            def to_string(self):
                string = ""
                i = 0
                for i, fun in enumerate(self.model):
                    if isinstance(fun, type):
                        string += "Layer {}: {}\n".format(i, fun.__name__)
                    else:
                        string += "Layer {}: {}\n".format(i, fun._get_name)
                return string

        return Net(config["layers"], config)

    def train_cifar(self, config):
        '''
        Creates a model and trains it for each iteration in `tune.run`. 
        Reports back to the hyperparameter optimizer the results from each iteration.

        Args:
            config: A JSON object containing the model arguments.
        '''
        net = Optimize.create_model_from_args(self, config)
        device = "cpu"
        if torch.cuda.is_available():
            device = "cuda:0"
            if torch.cuda.device_count() > 1:
                net = nn.DataParallel(net)
        net.to(device)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(net.parameters(), lr = config["lr"], momentum=0.9)

        data_dir = os.path.abspath("./data")
        trainset, testset = self.load_data(data_dir)

        test_abs = int(len(trainset) * 0.8)
        train_subset, val_subset = random_split(
            trainset, [test_abs, len(trainset) - test_abs])

        trainloader = torch.utils.data.DataLoader(
                train_subset,
                batch_size=int(config["batch_size"]),
                shuffle=True,
                num_workers=8
            )

        valloader = torch.utils.data.DataLoader(
                val_subset,
                batch_size=int(config["batch_size"]),
                shuffle=True,
                num_workers=8
            )

        for epoch in range(10):  # loop over the dataset multiple times
            running_loss = 0.0
            epoch_steps = 0
            for i, data in enumerate(trainloader, 0):
                # get the inputs; data is a list of [inputs, labels]
                inputs, labels = data
                inputs, labels = inputs.to(device), labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward + backward + optimize
                outputs = net(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                # print statistics
                running_loss += loss.item()
                epoch_steps += 1
                if i % 2000 == 1999:  # print every 2000 mini-batches
                    print("[%d, %5d] loss: %.3f" % (
                        epoch + 1, i + 1, running_loss / epoch_steps))
                    running_loss = 0.0
            # Validation loss
            val_loss = 0.0
            val_steps = 0
            total = 0
            correct = 0

            # Used in case we have parallel processing
            for i, data in enumerate(valloader, 0):
                with torch.no_grad():
                    inputs, labels = data
                    inputs, labels = inputs.to(device), labels.to(device)

                    outputs = net(inputs)
                    _, predicted = torch.max(outputs.data, 1)
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()

                    loss = criterion(outputs, labels)
                    val_loss += loss.cpu().numpy()
                    val_steps += 1

            # Report findings to ray for hyperparameter tuning/optimization
            tune.report(loss=(val_loss / val_steps), accuracy=correct / total)
        print("Training completed for model")

    def load_data(self, data_dir="./data"):
        """Loads cifar-10 dataset and divides them into train and test sets.
        
            Returns:
                Train and test set for use with pytorch model.
        """

        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

        # We add FileLock here because multiple workers will want to
        # download data, and this may cause overwrites since
        # DataLoader is not threadsafe.
        with FileLock(os.path.expanduser("~/.data.lock")):
            trainset = torchvision.datasets.CIFAR10(
                root=data_dir, train=True, download=True, transform=transform)

            testset = torchvision.datasets.CIFAR10(
                root=data_dir, train=False, download=True, transform=transform)

        return trainset, testset

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
            tune.with_parameters(self.train_cifar),
            resources_per_trial={"cpu": 2, "gpu": 1}, # For Google Colab Environment
            config=config,
            metric="loss",
            mode="min",
            num_samples=10,
            scheduler=scheduler
        )

        best_trial = result.get_best_trial("loss", "min", "last")
        print("Best trial config: {}".format(best_trial.config))
        print("Best trial final validation loss: {}".format(
            best_trial.last_result["loss"]))
        print("Best trial final validation accuracy: {}".format(
            best_trial.last_result["accuracy"]))

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


    
    
    