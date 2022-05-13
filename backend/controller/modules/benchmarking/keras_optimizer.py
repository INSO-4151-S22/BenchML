

from argparse import ArgumentTypeError

from keras.models import Sequential
from keras import layers
from keras.datasets import cifar10
from keras.utils import np_utils
from keras.optimizers import gradient_descent_v2

from ray import tune
class KerasOptimizer():

    def __init__(self):
        pass

    def create_model(self, config):
        """Creates a keras model based on given structure with the usage of config values in hyperparameters."""

        model = Sequential()
        try:
            # Define layers based on init args
            for layer in config["layers"]:
                layer_args = {}
                keyword_name = ''

                for i in range(1, len(layer)-1, 2):
                    keyword_name = layer[i]  # First is the keyword name and then the value for it
                    if isinstance(layer[i+1], str) and layer[i+1] in config.keys():
                        layer_args[keyword_name] = config[layer[i+1]]  # Applies a config value to it if available
                    elif isinstance(layer[i+1], list):  # It is a list of values so evalulate and store in keyword
                        tup = layer[i+1]
                        for i, item in enumerate(tup):
                            if isinstance(item, str) and item in config.keys():  # If string in config, then get original value
                                tup[i] = config[item]
                        layer_args[keyword_name] = tuple(tup)  # Store tuple in keyword_argument
                    else:
                        layer_args[keyword_name] = layer[i+1]
                
                layer_ = getattr(layers, layer[0])  # Create layer from string
                model.add(layer_(**layer_args))  # Create the instance from keyword arguments and save it in the layer list
        except:
            raise ArgumentTypeError("Some layers are incompatible with the optimization model creation for this current version.")

        return model

    def load_data(self, data_dir="./data"):
        """Loads cifar-10 dataset and divides them into train and test sets.
        
            Returns:
                Train and test set for use with pytorch model.
        """
        (X_train, y_train), (X_test, y_test) = cifar10.load_data()
        X_train = X_train.astype('float32') 
        X_test = X_test.astype('float32') 
        X_train = X_train / 255.0 
        X_test = X_test / 255.0
        y_train = np_utils.to_categorical(y_train, num_classes=10) 
        y_test = np_utils.to_categorical(y_test, num_classes=10) 

        return (X_train, y_train), (X_test, y_test)

    def train_tune(self, config):
        
        ds_train, ds_test = self.load_data()

        model: Sequential = self.create_model(config)

        decay = config["lr"]/100 
        sgd = gradient_descent_v2.SGD(learning_rate=config["lr"], momentum=0.9, decay=decay) 
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        # Report loss and accuracy to ray tune
        hist = model.fit(*ds_train, validation_data=ds_test, epochs=50, batch_size=config['batch_size'])

        tune.report(loss=(hist.history["val_loss"][-1]), accuracy=hist.history["val_accuracy"][-1]) 

    def train(self, config):
        """
        Gets a model and trains it using Keras and the CIFAR10 dataset.

        Args:
            model: A Keras model to be trained.

        Returns:
            Trained model.
        """

        ds_train, ds_test = self.load_data()

        model: Sequential = self.create_model(config)

        decay = 0.01/100 
        sgd = gradient_descent_v2.SGD(learning_rate=0.01, momentum=0.9, decay=decay) 
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        # Report loss and accuracy to ray tune
        model.fit(*ds_train, validation_data=ds_test, epochs=40, batch_size=16) 

        return model