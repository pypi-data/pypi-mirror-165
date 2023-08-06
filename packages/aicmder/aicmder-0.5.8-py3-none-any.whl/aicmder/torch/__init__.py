def freeze_parameter(model):
    for param in model.parameters():
        param.requires_grad = False


def train_params(model, verbose=False):
    params_to_update = []
    for name, param in model.named_parameters():
        if param.requires_grad == True:
            params_to_update.append(param)
            if verbose:
                print("\t", name)
    return params_to_update