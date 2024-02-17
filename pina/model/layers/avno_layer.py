"""Module for Averaging Neural Operator Layer class."""
from torch import nn, mean

class AVNOLayer(nn.Module):
    """
    The PINA implementation of the inner layer 
        of the Averaging Neural Operator . 

    :param int hidden_size: size of the layer.
    :param func: the activation function to use. 
    """
    def __init__(self, hidden_size: int, func=nn.GELU):
        super().__init__()
        self.hidden_size = hidden_size
        self.nn = nn.Linear(self.hidden_size, self.hidden_size)


    def forward(self, batch):
        """Forward pass of the layer."""
        return self.func()(self.nn(batch) + mean(batch, dim=1).unsqueeze(1))

    def linear_component(self, batch):
        """Linear component of the layer."""
        return self.nn(batch)
