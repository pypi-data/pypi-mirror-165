

def model_params(model):
    """
    Model params

    This function is used to count and display python model parameters.

    Parameters
    ----------
    model : nn.Module
        A python pytorch model that is inheriting from the nn.Module class.
        
    Returns
    -------
    None

    See Also
    --------
    categorical_accuracy: Calculates the categorical accuracy between the predicted labels and real labels.
    binary_accuracy: Calculate the binary accuracy between the predicted labels and real labels.
    
    Examples
    --------
    >>> model_params(my_model)
    TOTAL MODEL PARAMETERS: 	9,071,332
    TOTAL TRAINABLE PARAMETERS: 	9,071,332
    """
    n_params = sum(p.numel() for p in model.parameters())
    trainable_param = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"TOTAL MODEL PARAMETERS: \t{n_params}")
    print(f"TOTAL TRAINABLE PARAMETERS: \t{trainable_param}")
