

from argparse import ArgumentTypeError

import keras
from keras.models import Sequential
from keras import layers
from keras.datasets import cifar10
from keras.utils import np_utils
from keras.optimizers import gradient_descent_v2
from ray.tune.integration.keras import TuneReportCallback
from filelock import FileLock
import os

class KerasOptimizer():

    def __init__(self):
        pass

    def create_model(self, config):
        """Creates a keras model based on given structure with the usage of config values in hyperparameters."""

        self.model = Sequential()

        try:
            # Define layers based on init args
            for layer in layers:
                layer_args = {}
                keyword_name = ''

                for i in range(1, len(layer-1), 2):
                    keyword_name = layer[i]  # First is the keyword name and then the value for it
                    if isinstance(layer[i+1], str) and config[layer[i+1]]:
                        layer_args[keyword_name] = config[layer[i+1]]  # Applies a config value to it if available
                    else:
                        layer_args[keyword_name] = layer[i]
                layer_ = getattr(layers, layer[0])  # Create layer from string
                self.model.add(layer_(**layer_args))  # Create the instance from keyword arguments and save it in the layer list
        except:
            raise ArgumentTypeError("Some layers are incompatible with the optimization model creation for this current version.")

        return self.model

    def train(self, config):
        with FileLock(os.path.expanduser("~/.data.lock")):
            (X_train, y_train), (X_test, y_test) = cifar10.load_data()
        X_train = X_train.astype('float32') 
        X_test = X_test.astype('float32') 
        X_train = X_train / 255.0 
        X_test = X_test / 255.0
        y_train = np_utils.to_categorical(y_train) 
        y_test = np_utils.to_categorical(y_test) 

        model = self.create_model(config)

        decay = config["lr"]/100 
        sgd = gradient_descent_v2.SGD(lr=config["lr"], momentum=0.9, decay=decay) 
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['loss', 'accuracy'])

        # Report loss and accuracy to ray tune
        model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=config['batch_size'], 
            callbacks=[TuneReportCallback({"mean_accuracy": "accuracy"})],) 
