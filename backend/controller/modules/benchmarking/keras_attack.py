import tensorflow as tf
import numpy as np
import random

class KerasAttack():

    def __init__(self, model, ds_train, ds_test):
        self.model = model
        (self.X_train, self.y_train), (self.X_test, self.y_test) = (ds_train, ds_test)

    
    def adversarial_pattern(self, image, label):
        image = tf.cast(image, tf.float32)
        
        with tf.GradientTape() as tape:
            tape.watch(image)
            prediction = self.model(image)
            loss = tf.keras.losses.MSE(label, prediction)
        
        gradient = tape.gradient(loss, image)
        
        signed_grad = tf.sign(gradient)
        
        return signed_grad


    def generate_adversarials(self, batch_size, X_train, Y_train):
        while True:
            x = []
            y = []
            for batch in range(batch_size):
                N = random.randint(0, 100)

                label = Y_train[N]
                image = X_train[N]
                
                perturbations = self.adversarial_pattern(image.reshape((1, 32, 32, 3)), label).numpy()
                
                
                epsilon = 0.1
                adversarial = image + perturbations * epsilon
                
                x.append(adversarial)
                y.append(Y_train[N])
            
            
            x = np.asarray(x).reshape((batch_size, 32, 32, 3))
            y = np.asarray(y)
            
            yield x, y
    