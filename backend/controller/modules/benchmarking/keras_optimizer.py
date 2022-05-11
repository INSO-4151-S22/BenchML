

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
import ast
import tensorflow as tf
import tensorflow_datasets as tfds

class KerasOptimizer():

    def __init__(self):
        pass

    def create_model(self, config):
        """Creates a keras model based on given structure with the usage of config values in hyperparameters."""

        model = Sequential()
        
        try:
            # Define layers based on init args
            for layer in layers:
                layer_args = {}
                keyword_name = ''
                
                for i in range(1, len(layer-1), 2):
                    keyword_name = layer[i]  # First is the keyword name and then the value for it
                    if isinstance(layer[i+1], str) and config[layer[i+1]]:
                        layer_args[keyword_name] = config[layer[i+1]]  # Applies a config value to it if available
                    elif isinstance(layer[i+1], str) and str(layer[i+1]).startswith("["):  # It is a list of values so evalulate and store in keyword
                        tup = ast.literal_eval(layer[i+1])  # Get list with values to turn into tuple
                        for i, item in enumerate(tup):
                            if isinstance(item, str) and config[item]:  # If string in config, then get original value
                                tup[i] = config[item]
                        layer_args[keyword_name] = tuple(tup)  # Store tuple in keyword_argument
                    else:
                        layer_args[keyword_name] = layer[i]
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
        with FileLock(os.path.expanduser("~/.data.lock")):
            (ds_train, ds_test), ds_info = tfds.load(
                'cifar-10',
                data_dir=data_dir,
                split=['train', 'test'],
                shuffle_files=True,
                as_supervised=True,
                with_info=True,
            )

        def normalize_img(image, label):
            """Normalizes images: `uint8` -> `float32`."""
            return tf.cast(image, tf.float32) / 255., label

        ds_train = ds_train.map(
            normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
        ds_train = ds_train.cache()
        ds_train = ds_train.shuffle(ds_info.splits['train'].num_examples)

        ds_test = ds_test.map(
            normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
        ds_test = ds_test.cache()
        ds_test = ds_test.prefetch(tf.data.AUTOTUNE)


        return ds_train, ds_test

    def train_tune(self, config):
        
        ds_train, ds_test = self.load_data()

        model: Sequential = self.create_model(config)

        decay = config["lr"]/100 
        sgd = gradient_descent_v2.SGD(lr=config["lr"], momentum=0.9, decay=decay) 
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['loss', 'accuracy'])

        # Report loss and accuracy to ray tune
        model.fit(ds_train, validation_data=ds_test, epochs=50, batch_size=config['batch_size'], 
            callbacks=[TuneReportCallback({"mean_accuracy": "accuracy"})],) 

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
        sgd = gradient_descent_v2.SGD(lr=0.01, momentum=0.9, decay=decay) 
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['loss', 'accuracy'])

        # Report loss and accuracy to ray tune
        model.fit(ds_train, validation_data=ds_test, epochs=50, batch_size=16) 

        return model