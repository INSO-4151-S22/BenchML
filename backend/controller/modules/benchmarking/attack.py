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
            return KerasAttack()
        elif self.model_type == 'pytorch':
            return PyTorchAttack(model)
        else: 
            raise Exception(f"No attacker available for {self.model_type}")


    def run(self, url):
        # Get config from the url
        config = self.op.get_model_config(url)
        # Use config in train to create a model, train it, and return it
        print("Training model:")
        self.model = self.op.optimizer.train(config)
        self.attacker = self.get_attacker(self.model)
        return self.eval_model()
        

    def _accuracy(self, logits, target):
        _, pred = torch.max(logits, dim=1)
        correct = (pred == target).sum()
        total = target.size(0)
        acc = (float(correct) / total) * 100
        return acc


    def eval_model(self):
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