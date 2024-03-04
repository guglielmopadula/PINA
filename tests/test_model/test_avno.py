import torch
from pina.model import AVNO
from pina import LabelTensor

output_channels = 5
batch_size = 15


def test_constructor():
    input_channels = 1
    output_channels = 1
    #minimuum constructor
    AVNO(input_channels,
         output_channels,
         coordinates_indices='p',
         field_indices='v')

    #all constructor
    AVNO(input_channels,
         output_channels,
         inner_size=5,
         n_layers=5,
         func=torch.nn.ReLU,
         coordinates_indices='p',
         field_indices='v')


def test_forward():
    input_channels = 1
    output_channels = 1
    points_size = 1
    input_ = LabelTensor(
        torch.rand(batch_size, 1000, input_channels + points_size),
        ['p_0', 'v_0'])
    ano = AVNO(input_channels,
               output_channels,
               points_size=points_size,
               coordinates_indices='p',
               field_indices='v')
    out = ano(input_)
    assert out.shape == torch.Size(
        [batch_size, input_.shape[1], output_channels])


def test_backward():
    input_channels = 1
    points_size = 1
    output_channels = 1
    input_ = LabelTensor(
        torch.rand(batch_size, 1000, points_size + input_channels),
        ['p_0', 'v_0'])
    input_ = input_.requires_grad_()
    avno = AVNO(input_channels,
                output_channels,
                points_size=points_size,
                coordinates_indices='p',
                field_indices='v')
    out = avno(input_)
    tmp = torch.linalg.norm(out)
    tmp.backward()
    grad = input_.grad
    assert grad.shape == torch.Size(
        [batch_size, input_.shape[1], points_size + input_channels])
