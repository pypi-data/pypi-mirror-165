### helperfns

🎀 This is a python package that contains some helper functions for machine leaning.

<p align="center">
   <img src="https://github.com/CrispenGari/helperfns/blob/main/images/logo.png" alt="logo" width="60%"/>
</p>

### Getting started

To start using `helperfns` in your project you run the following command:

```shell
pip install helperfns
```

Or if you wan to install it in notebooks such as jupyter notebooks you can run the code cell with the following code:

```shell
!pip install helperfns
```

### Usage

The `helperfns` package is made up of different sub packages such as:

1. tables
2. text
3. utils
4. visualization
5. torch

### tables

In the tables sub package you can print your data in tabular form for example:

```python
from helperfns.tables import tabulate_data

column_names = ["SUBSET", "EXAMPLE(s)", "Hello"]
row_data = [["training", 5, 4],['validation', 4, 4],['test', 3, '']]
tabulate_data(column_names, row_data)

```

Output:

```shell
+---------------------------------+
|              Table              |
+------------+------------+-------+
| SUBSET     | EXAMPLE(s) | Hello |
+------------+------------+-------+
| training   |          5 |     4 |
| validation |          4 |     4 |
| test       |          3 |       |
+------------+------------+-------+
```

### text

The text package offers two main function which are `clean_sentence`, `de_contract`, `generate_ngrams` and `generate_bigrams`

```python
from helperfns.text import *

# cleans the sentence
print(clean_sentence("text 1 # https://url.com/bla1/blah1/"))
# list of all english words
print(english_words)
# converts strings like `I'm` to 'I am'
print(de_contract("I'm"))

# generate bigrams from a list of word
print(text.generate_bigrams(['This', 'film', 'is', 'terrible']))

# generates n-grams from a list of words
print(text.generate_ngrams(['This', 'film', 'is', 'terrible']))
```

### utils

utils package comes with a simple helper function for converting seconds to hours, minutes and seconds.

Example:

```python
start = time.time()
for i in range(100000):
   pass
end = time.time()

```

Output:

```shell
'0:00:00.01'
```

### visualization

This sub package provides different helper functions for visualizing data using plots.

Examples:

```python
from helperfns.visualization import plot_complicated_confusion_matrix, plot_images, plot_images_predictions, plot_simple_confusion_matrix

# plot predicted image labels with the images
plot_images_predictions(images, true_labels, preds, classes=["dog", "cat"] ,cols=8)

# plot the images with their labels
plot_images(images[:24], true_labels[:24], cols=8)

# plot a simple confusion matrix
y_true = [random.randint(0, 1) for _ in range (100)]
y_pred = [random.randint(0, 1) for _ in range (100)]
classes =["dog", "cat"]
plot_simple_confusion_matrix(y_true, y_pred, classes)

# plot a confusion matrix with percentage value of confusion
y_true = [random.randint(0, 1) for _ in range (100)]
y_pred = [random.randint(0, 1) for _ in range (100)]
classes =["dog", "cat"]
plot_complicated_confusion_matrix(y_true, y_pred, classes)
```

### torch

This is a subpackage that contains other subpackages mainly used when working with `pytorch`. These sub packages are:

1. text
2. models
3. accuracy

### `torch.text`

This package contains the `label_pipeline` and `text_pipeline`. This helper function are normally used when doing text processing in python pytorch.

Example:

```python
from helperfns.torch import text

# converting a sentence into sequence of integer representation.
vocab = {'<unk>': 0, 'this': 1, 'is': 2, 'a': 3, 'dog': 4}
tokenizer = lambda x: x.split(' ')
print(text.text_pipeline("This is a dog that is backing", tokenizer=tokenizer, vocab=vocab, unk_token='<unk>', lower=True))

# converting labels into their integer representation.
labels_dict = {l:i for (i, l) in enumerate(['af', 'en', 'st', 'ts', 'xh', 'zu'])}
print(text.label_pipeline("en", labels_dict=labels_dict))

```

### `torch.models`

This package contains a helper function called `model_params`. This function is used to count the model parameters of a pytorch model. Example:

```python
model_params(my_model)
```

> Note that `my_model` is a python class model instance that is inheriting from the `nn.Module` class.

### `torch.accuracy`

This package contains two helper functions called that are used to calculate the accuracy between predicted labels and real label. These functions are:

1. `binary_accuracy` - used to calculate the binary accuracy between predicted labels and real labels.

```python
y = y.to(device)
predictions = model(X).squeeze(1)
loss = criterion(predictions, y)
acc = binary_accuracy(predictions, y)
print(acc)
```

2. `categorical_accuracy` - used to calculate the categorical accuracy between predicted labels and real labels.

```python
y = y.to(device)
predictions = model(X).squeeze(1)
loss = criterion(predictions, y)
acc = categorical_accuracy(predictions, y)
print(acc)
```

### Contributing to `helperfns`.

To contribute to `helperfns` read the [CONTRIBUTION.md](https://github.com/CrispenGari/helperfns/blob/main/CONTRIBUTION.md) file.

### License

In this package the `MIT` license was used which reads as follows:

```
MIT License

Copyright (c) 2022 crispengari

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
