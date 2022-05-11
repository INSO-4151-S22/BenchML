import torch
import torch.nn.functional as F


class KerasAttack():

    def __init__(self, model, target=None):
        self.target = target
        self.model = model
        self.attack_steps = 7
        self.attack_lr = 2.0

    def forward(self, x, y):
        """
        :param x: Inputs to perturb
        :param y: Ground-truth label
        :param target : Target label 
        :return adversarial image
        """
        x_adv = x.detach().clone()

        for _ in range(self.attack_steps):
            x_adv.requires_grad = True
            self.model.zero_grad()
            logits = self.model(x_adv)
            if self.target is None:
                # Untargetted attack
                loss = F.cross_entropy(logits, y,  reduction="sum")
                loss.backward()                      
                grad = x_adv.grad.detach()
                grad = grad.sign()
                x_adv = x_adv + self.attack_lr * grad

            # Projection
            x_adv = x + torch.clamp(x_adv - x, min=-8.0, max=8.0)
            x_adv = x_adv.detach()
            x_adv = torch.clamp(x_adv, 0, 1)

        return x_adv

    def __call__(self, x, y):
        x_adv = self.forward(x,y)
        return x_adv