from argparse import ArgumentTypeError
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import random_split, DataLoader
import torchvision
import torch.optim as optim
import torchvision.transforms as transforms
from filelock import FileLock
import os
from ray import tune

class PyTorchOptimizer():

    def __init__(self):
        pass

    def create_model(self, config):
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
                def __init__(self):
                    super(Reshape, self).__init__()

                def forward(self, x):
                    return x.view(x.size(0), -1)

            class Net(nn.Module):
                
                def __init__(self, layers, config):
                    super().__init__()
                    # Define layers based on init Args
                    self.model = nn.ModuleList()
                    try:
                        for layer in layers:
                            print(f"layer: {layer}")
                            module_ = None
                            if len(layer) > 0:  # Modules that are part of the torch nn import
                                layer_args = []
                                for i in range(1, len(layer)):
                                    if isinstance(layer[i], str) and config[layer[i]]:
                                        layer_args.append(config[layer[i]])  # Applies a config value to it if available
                                    else:
                                        layer_args.append(layer[i])
                                if layer[0] == 'Reshape':  # Custom module not in nn
                                    module_ = Reshape
                                else:
                                    module_ = getattr(nn, layer[0])  # Create module from string
                                self.model.append(module_(*layer_args))  # Create the instance and save it in the module list
                    except:
                        raise ArgumentTypeError("Some layers are incompatible with the optimization model creation for this current version.")

                def forward(self, x):
                    # Define forward function based on init args 
                    for fun in self.model:
                        x = fun(x)
                    return x

            return Net(config["layers"], config)


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


    def train_tune(self, config):
        """
        Creates a model with the config provided and trains it using PyTorch and the CIFAR10 dataset.

        Args:
            config: A JSON object containing the model arguments.

        Returns:
            Tuple containing the loss and accuracy for the trained model.
        """
        net = self.create_model(config)

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

        trainloader = DataLoader(
                train_subset,
                batch_size=int(config["batch_size"]),
                shuffle=True,
                num_workers=8
            )

        valloader = DataLoader(
                val_subset,
                batch_size=int(config["batch_size"]),
                shuffle=True,
                num_workers=8
            )

        for epoch in range(5):  # loop over the dataset multiple times
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

        # Report loss and accuracy to ray tune
        tune.report(loss=(val_loss / val_steps), accuracy=correct / total)
        print(f"loss: {(val_loss / val_steps)}, acc: {correct / total}")


    def train(self, config):
        """
        Gets a model and trains it using PyTorch and the CIFAR10 dataset.

        Args:
            model: A PyTorch model to be trained.

        Returns:
            Trained model.
        """
        net = self.create_model(config)

        device = "cpu"
        if torch.cuda.is_available():
            device = "cuda:0"
            if torch.cuda.device_count() > 1:
                net = nn.DataParallel(net)
        net.to(device)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(net.parameters(), lr = 0.01, momentum=0.9)

        data_dir = os.path.abspath("./data")
        trainset, testset = self.load_data(data_dir)

        test_abs = int(len(trainset) * 0.8)
        train_subset, val_subset = random_split(
            trainset, [test_abs, len(trainset) - test_abs])

        trainloader = DataLoader(
                train_subset,
                batch_size=int(16),
                shuffle=True,
                num_workers=8
            )

        valloader = DataLoader(
                val_subset,
                batch_size=int(16),
                shuffle=True,
                num_workers=8
            )

        for epoch in range(5):  # loop over the dataset multiple times
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
                if i % 100 == 0:  # print every 2000 mini-batches
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

        print(f"loss: {(val_loss / val_steps)}, acc: {correct / total}")
        return net