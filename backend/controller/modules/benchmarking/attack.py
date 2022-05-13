from backend.controller.modules.benchmarking.optimize import Optimize
from backend.controller.modules.benchmarking.pytorch_attack import PyTorchAttack
from backend.controller.modules.benchmarking.keras_attack import KerasAttack
import torch
import torch.utils.data
class Attack():

    def __init__(self, resources = {'cpu': 2, 'gpu' : 0}, model_type = None):
        self.resources = resources
        self.model_type = model_type
        self.op = Optimize(self.resources, self.model_type)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'


    def get_attacker(self, model):
        """Based on the model type in config, create an aa model to be attacked with adversarial learning."""
        if self.model_type == 'keras':
            ds_train, ds_test = self.op.optimizer.load_data()
            return KerasAttack(model, ds_train, ds_test)
        elif self.model_type == 'pytorch':
            return PyTorchAttack(model)
        else: 
            raise Exception(f"No attacker available for {self.model_type}")


    def run(self, url):
        # Get config from the url
        config = self.op.get_model_config(url)
        # Use config in train to create a model, train it, and return it
        self.model = self.op.optimizer.train(config)
        if self.model_type == 'pytorch':
            self.attacker = self.get_attacker(self.model)
            return self.eval_pytorch_model()
        elif self.model_type == 'keras':
            self.attacker = self.get_attacker(self.model)
            return self.eval_keras_model(self.attacker.X_train, self.attacker.y_train, self.attacker.X_test, self.attacker.y_test)
        else: 
            raise Exception(f"No attacker available for {self.model_type}")
        

    def _accuracy(self, logits, target):
        _, pred = torch.max(logits, dim=1)
        correct = (pred == target).sum()
        total = target.size(0)
        acc = (float(correct) / total) * 100
        return acc


    def eval_pytorch_model(self):
        self.model.eval()
        acc = 0 
        adv_acc = 0 
        _, dstest = self.op.optimizer.load_data()
        testloader = torch.utils.data.DataLoader(
            dstest,
            batch_size=int(16),
            shuffle=True,
            num_workers=8
        )
        for i, (x,y) in enumerate(testloader):
            x, y = x.to(self.device), y.to(self.device)
            x_adv = self.attacker(x,y)
            logits = self.model(x)
            adv_logits = self.model(x_adv)
            acc += self._accuracy(logits, y)
            adv_acc += self._accuracy(adv_logits, y)

        return acc/(i+1), adv_acc/(i+1)

    def eval_keras_model(self, X_train, y_train, X_test, y_test):

        # Model evaluation without adversarial perturbation
        acc = self.model.evaluate(x=X_test, y=y_test, verbose=0)[1]
        x_adversarial_train, y_adversarial_train = next(self.attacker.generate_adversarials(20000, X_train, y_train))  # Used for defending against adversarial attack
        x_adversarial_test, y_adversarial_test = next(self.attacker.generate_adversarials(10000, X_test, y_test))
        # Evaluate against adversarial samples
        adv_acc = self.model.evaluate(x=x_adversarial_test, y=y_adversarial_test, verbose=0) 
        return acc, adv_acc