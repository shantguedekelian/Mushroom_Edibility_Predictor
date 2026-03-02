import torch.nn as nn
from torchvision import models
from torchvision.models import ResNet18_Weights

def get_model(num_classes=2):
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model
