from turtle import turtles
import matplotlib.pyplot as plt
import itertools
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np

def plot_simple_confusion_matrix(
    y_true:list, 
    y_pred:list, 
    classes:list=[], 
    figsize:tuple=(10, 10), 
    fontsize: int = 15
):
    """
    Plot Complicated Confusion Matrix 

    This function simply plots a confusion matrix.

    Parameters
    ----------
    y_true : list
        Takes in a collection of true labels.
    y_pred : list
        Takes in a collection of predicted labels.
    
    Keyword Args
    ------------
    classes : list
        A list of class name e.g ['dog', 'cat'] default is y_true.
    figsize : tuple
        The figsize of the confusion matrix plot default is (10, 10);
    fontsize : int
        Font size for the contents of the confusion matrix, default is 15.
        
    Returns
    -------
    None

    See Also
    --------
    plot_complicated_confusion_matrix : Plots a confusion matrix with some percentage(%) of confusion.
    plot_images: Plots the images and display them.
    plot_images_predictions: Plots the images with their predictions and display them.
    
    Examples
    --------
    >>> y_true = [random.randint(0, 1) for _ in range (100)]
    >>> y_pred = [random.randint(0, 1) for _ in range (100)]
    >>> classes =["dog", "cat"]
    >>> plot_complicated_confusion_matrix(y_true, y_pred, classes)
    """
    assert len(y_true) == len(y_pred), f"The length of predicted and real labels must be equal, received {len(y_pred)} and {len(y_true)}."

    fig = plt.figure(figsize = figsize)
    ax = fig.add_subplot(1, 1, 1)
    cm = confusion_matrix(y_true, y_pred)

    if len(classes) == 0:
        classes = list(set(y_true))

    cm = ConfusionMatrixDisplay(cm, display_labels= classes)
    cm.plot(values_format = 'd', cmap = 'Blues', ax = ax)
    plt.xticks(rotation = 20, color="black", fontsize=fontsize)
    plt.yticks(rotation = 20, color="black", fontsize=fontsize)
    plt.show()

def plot_complicated_confusion_matrix(y_true:list, y_pred:list, 
                                    classes:list=[], 
                                    figsize:turtles=(5, 5), 
                                    fontsize:int=20,
                                    title:str="Confusion Matrix",
                                    xlabel:str="Predicted label",
                                    ylabel:str="True label",
                                      ):
    
    """
    Plot Complicated Confusion Matrix 

    This function simply plots a confusion matrix with some percentage(%) of confusion between class labels.

    Parameters
    ----------
    y_true : list
        Takes in a collection of true labels.
    y_pred : list
        Takes in a collection of predicted labels.
    
    Keyword Args
    ------------
    classes : list
        A list of class name e.g ['dog', 'cat'].
    figsize : turple
        The figsize of the confusion matrix plot
    title : str
        The title to display for the confusion matrix, default is 'Confusion Matrix' .
    xlabel : str
        The x-axis label, default is 'True label'.
    ylabel : str
        The y-axis label, default is 'Predicted label'.
    fontsize : int
        Font size for the contents of the confusion matrix, default is 20.
        
    Returns
    -------
    None

    See Also
    --------
    plot_simple_confusion_matrix : Plots a simple confusion matrix.
    plot_images: Plots the images and display them.
    plot_images_predictions: Plots the images with their predictions and display them.
    
    Examples
    --------
    >>> y_true = [random.randint(0, 1) for _ in range (100)]
    >>> y_pred = [random.randint(0, 1) for _ in range (100)]
    >>> classes =["dog", "cat"]
    >>> plot_simple_confusion_matrix(y_true, y_pred, classes)
    """
    
    assert len(y_true) == len(y_pred), f"The length of predicted and real labels must be equal, received {len(y_pred)} and {len(y_true)}."
    cm = confusion_matrix(y_true, y_pred)
    cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
    n_classes = cm.shape[0]

    fig, ax = plt.subplots(figsize=figsize)
    cax = ax.matshow(cm, cmap=plt.cm.Blues)
    fig.colorbar(cax)

    if len(classes):
        labels = classes
    else:
        labels = np.arange(cm.shape[0])

    ax.set(
         title=title,
         xlabel=xlabel,
         ylabel=ylabel,
         xticks=np.arange(n_classes),
         yticks=np.arange(n_classes),
         xticklabels=labels,
         yticklabels=labels,
          )
    ax.yaxis.label.set_color('green')
    ax.xaxis.label.set_color('green')


    ax.xaxis.set_label_position("bottom")
    ax.xaxis.tick_bottom()

    threshold = (cm.max() + cm.min()) / 2.
    # Plot the text on each cell
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, f"{cm[i, j]} ({cm_norm[i, j]*100:.1f}%)",
                 horizontalalignment="center",
                 color="white" if cm[i, j] > threshold else "black",
                 size=fontsize)
    plt.show()

def plot_images(images:list, labels:list, cols:int=5, rows: int=3, fontsize: int=16)->None:
    """
    Plot images 

    This function simply plots Images with their labels.

    Parameters
    ----------
    images : list
        Takes in a collection of images.
    labels : list
        Takes in a collection of image labels.
    
    Keyword Args
    ------------
    cols : int
        Number of columns for images, default is 5.
    rows : int
        Number of rows for images, default is 3
    fontsize : int
        Font size for labels, default is 16.
        
    Returns
    -------
    None

    See Also
    --------
    plot_complicated_confusion_matrix : Plots a confusion matrix with some percentage(%) of confusion.
    plot_simple_confusion_matrix : Plots a simple confusion matrix.
    plot_images_predictions: Plots the images with their predictions and display them.
    
    Examples
    --------
    >>> plot_images(images[:24], true_labels[:24], cols=8)
    """
    
    assert len(images) == len(labels), f"The length for images and labels must match but got {len(images)} {len(labels)}"
    
    fig = plt.figure()
    fig.set_size_inches(cols * 2, rows * 2)
    for i, (image, label) in enumerate(zip(images, labels)):
        plt.subplot(rows, cols, i + 1)
        plt.axis('off')
        plt.imshow(image, cmap="gray")
        plt.title(label, color ='g', fontsize=fontsize )
        
    plt.show()


def plot_images_predictions(images:list, labels_true:list, 
                            labels_pred:list, classes:list=[], cols:int=5,
                            rows:int = 3, fontsize:int=16):
    """
    Plot images predictions

    This function simply plots predicted images. Images with wrongly predicted labels their
    labels will be red and green otherwise. 

    Parameters
    ----------
    images : list
        Takes in a collection of images.
    labels_true : list
        Takes in a collection of correct labels.
    labels_pred : list
        Takes in a collection of predicted labels.
        
    Keyword Args
    ------------
    classes : list
        Takes in a collection  of class labels example can be ['cat', 'dog'] if 
        not passed then labels_pred will be used.
    cols : int
        Number of columns for images, default is 5.
    rows : int
        Number of rows for images, default is 3
    fontsize : int
        Font size for labels, default is 16.
        
    Returns
    -------
    None

    See Also
    --------
    plot_complicated_confusion_matrix : Plots a confusion matrix with some percentage(%) of confusion.
    plot_simple_confusion_matrix : Plots a simple confusion matrix.
    plot_images: Plots the images and display them.

    Examples
    --------
    >>> plot_images_predictions(images, true_labels, preds, classes=["dog", "cat"] ,cols=8)

    """
    assert len(images) == len(labels_true) == len(labels_pred), f"The image classes, true labels and predicted labels must be equal but received {len(images)}, {len(labels_true)} and {len(labels_pred)}."
    
    fig = plt.figure()
    fig.set_size_inches(cols * 2, rows * 2)
    if len(classes):
        classes = classes
    else:
        classes = list(set(label_pred))
        
    for i, (image, label_true, label_pred) in enumerate(zip(images, labels_true, labels_pred)):
        plt.subplot(rows, cols, i + 1)
        plt.axis('off')
        plt.imshow(image, cmap="gray")
        plt.title(classes[label_true], color ='g' if label_true == label_pred else 'r', fontsize=fontsize )
        
    plt.show()   
        
        
        
        