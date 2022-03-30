"""Module for operators vectorize implementation"""
import torch

from pina.label_tensor import LabelTensor


def grad(output_, input_):
    """
    TODO
    """
    if not isinstance(input_, LabelTensor):
        raise TypeError

    gradients = torch.autograd.grad(
        output_,
        input_,
        grad_outputs=torch.ones(output_.size()).to(
            dtype=input_.dtype,
            device=input_.device),
        create_graph=True, retain_graph=True, allow_unused=True)[0]
    return LabelTensor(gradients, input_.labels)


def div(output_, input_):
    """
    TODO
    """
    if output_.shape[1] == 1:
        div = grad(output_, input_).sum(axis=1)
    else:  # really to improve
        a = []
        for o in output_.T:
            a.append(grad(o, input_))
        div = torch.zeros(output_.shape[0], 1)
        for i in range(output_.shape[1]):
            div += a[i][:, i].reshape(-1, 1)

    return div


def nabla(output_, input_):
    """
    TODO
    """
    return div(grad(output_, input_), input_)
