import pickle
from copy import deepcopy
from thop import profile
import torch
import pickle
import os


def torch_info():
    print('Pytorch version\t:', torch.__version__)
    print('CUDA version\t:', torch.version.cuda)
    print('GPU\t\t:', torch.cuda.get_device_name())


def save_batch(batch, filename="batch.pkl"):
    with open(filename, 'wb') as outp:
        pickle.dump(batch, outp, pickle.HIGHEST_PROTOCOL)


def model_info(model, pickle_path="batch.pkl", verbose=False):

    n_p = sum(x.numel() for x in model.parameters())  # number parameters
    n_g = sum(x.numel() for x in model.parameters() if x.requires_grad)  # number gradients

    if verbose:
        print(f"{'layer':>5} {'name':>40} {'gradient':>9} {'parameters':>12} {'shape':>20} {'mu':>10} {'sigma':>10}")
        for i, (name, p) in enumerate(model.named_parameters()):
            name = name.replace('module_list.', '')
            print('%5g %40s %9s %12g %20s %10.3g %10.3g' % (i, name, p.requires_grad, p.numel(), list(p.shape), p.mean(), p.std()))
    try:
        fs = ''

        if pickle_path is not None and os.path.exists(pickle_path):
            with open(pickle_path, 'rb') as inp:
                model_input = pickle.load(inp)
                if isinstance(model_input, list):
                    model_input = [data.to(next(model.parameters()).device) for data in model_input]
                else:
                    model_input.to(next(model.parameters()).device)
        else:
            first_parameter = next(model.parameters())
            input_shape = first_parameter.size()
            model_input = torch.zeros(input_shape, device=next(model.parameters()).device).contiguous()  # input
        if isinstance(model_input, list):
            flops = profile(deepcopy(model), inputs=model_input, verbose=False)[0] / 1E9 * 2
        else:
            flops = profile(deepcopy(model), inputs=(model_input,), verbose=False)[0] / 1E9 * 2
        fs = ', %.1f GFLOPs' % (flops)
    except Exception as e:
        print(e)
        fs = ''

    print(f"summary: {len(list(model.modules()))} layers, {n_p} parameters, {n_g} gradients{fs}")
