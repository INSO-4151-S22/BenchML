import torch
import torch.nn.functional as F


class PyTorchAttack():

    def __init__(self, model):
        self.model = model
        self.attack_name = "FGSM"


    def forward(self, x, y):
        """
        :param x: Inputs to perturb
        :param y: Ground-truth label
        :return adversarial image
        """
        x_adv = x.detach().clone()

        x_adv.requires_grad=True
        self.model.zero_grad()

        logit = self.model(x_adv)

        cost = -F.cross_entropy(logit, y)
        
        if x_adv.grad is not None:
            x_adv.grad.data.fill_(0)
        cost.backward()

        x_adv.grad.sign_()
        x_adv = x_adv - 8.0*x_adv.grad
        x_adv = torch.clamp(x_adv,*(0,1))

        return x_adv
    

    def __call__(self, x, y):
        x_adv = self.forward(x,y)
        return x_adv