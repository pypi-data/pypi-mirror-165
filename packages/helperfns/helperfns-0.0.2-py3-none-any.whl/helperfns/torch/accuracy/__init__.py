import torch

def binary_accuracy(y_preds, y_true)->float:
    """
    binary_accuracy

    This function calculates the binary accuracy between the predicted label and true labels.

    Parameters
    ----------
    y_preds : Tensor
        A torch tensor that contains predicted values.
    y_true : Tensor
        A torch tensor with real labels.
        
    Returns
    -------
    accuracy: float
        A float number between 0 and 1 for the accuracy.

    See Also
    --------
    categorical_accuracy: Calculates the categorical accuracy between the predicted labels and real labels.
    
    Examples
    --------
    >>> y = y.to(device)
    >>> predictions = model(X).squeeze(1)
    >>> loss = criterion(predictions, y)
    >>> acc = binary_accuracy(predictions, y)
    >>> print(acc)
    0.97
    """
    rounded_preds = torch.round(torch.sigmoid(y_preds))
    correct = (rounded_preds == y_true).float()
    return correct.sum() / len(correct)

def categorical_accuracy(y_preds, y)->float:
    """
    categorical_accuracy

    This function calculates the categorical accuracy between the predicted label and true labels.

    Parameters
    ----------
    y_preds : Tensor
        A torch tensor that contains predicted values.
    y_true : Tensor
        A torch tensor with real labels.
        
    Returns
    -------
    accuracy: float
        A float number between 0 and 1 for the accuracy.

    See Also
    --------
    binary_accuracy: Calculate the binary accuracy between the predicted labels and real labels.
    
    Examples
    --------
    >>> y = y.to(device)
    >>> predictions = model(X).squeeze(1)
    >>> loss = criterion(predictions, y)
    >>> acc = categorical_accuracy(predictions, y)
    >>> print(acc)
    0.97
    """
    top_pred = y_preds.argmax(1, keepdim = True)
    correct = top_pred.eq(y.view_as(top_pred)).sum()
    return  correct.float() / y.shape[0]
