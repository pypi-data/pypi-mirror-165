import torch

def text_pipeline(sent:str, tokenizer, vocab, unk_token:str, lower:bool=False):
    """
    Text Pipeline

    This function converts sentence to tokens of integers.

    Parameters
    ----------
    sent : str
        A string sentence or text to be tokenized and converted to integer tokens.
    tokenizer : function
        A tokenizer function to tokenize sentence into a sequence of words.
    vocab : dict
        A dictionary or that contains word to index mapping also known as the dictionary.
    unk_token : str
        A string which is the token for the unknown words in the vocab. This token must exist in your vocab object.
    lower : bool
        A boolean weather to convert the sentence to lower case before being tokenized, default is false.
        
    Returns
    -------
    values: list
        A list integers.

    See Also
    --------
    label_pipeline: Convert string label to an integer representation of that label.
    
    Examples
    --------
    >>> vocab = {'<unk>': 0, 'this': 1, 'is': 2, 'a': 3, 'dog': 4}
    >>> tokenizer = lambda x: x.split(' ')
    >>> print(text_pipeline("This is a dog that is backing", tokenizer=tokenizer, vocab=vocab, unk_token='<unk>', lower=True))
    [1, 2, 3, 4, 0, 2, 0]
    """
    values = list()
    tokens = tokenizer(sent.lower() if lower else sent)
    for token in tokens:
        try:
            v = vocab[token]
        except KeyError as e:
            v = vocab[unk_token]
        values.append(v)
    return values


def label_pipeline(label:str, labels_dict: dict)->int:
    """
    Label Pipeline

    This function converts a label into it's integer representation.

    Parameters
    ----------
    label : str
        A string label to be converted to an integer representation.
    labels_dict : dict
        A dictionary that contains label to index for labels.
           
    Returns
    -------
    label: int
        An integer label representation from a string.

    See Also
    --------
    text_pipeline: Converts text sentence to a sequence of integers.
    
    Examples
    --------
    >>> labels_dict = {l:i for (i, l) in enumerate(['af', 'en', 'st', 'ts', 'xh', 'zu'])}
    >>> print(text.label_pipeline("en", labels_dict=labels_dict))
    1
    """
    return labels_dict.get(label)
  
# def tokenize_batch(batch, text_pipeline, label_pipeline, max_len=50, padding="pre", binary_label: bool = True):
#     """
#     Tokenize Batch

#     This function tokenize a sentence and preprocess a single example in a batch by returning an integer representation of a label as well as integer representation of sequence of words as torch tensors.

#     Parameters
#     ----------
#     batch : list | numpy array
#         A  .
#     text_pipeline : function
#         A text pre-processing function that converts a sentence into sequence of integers.
#     label_pipeline : function
#         A label pre-processing function that a label into it's integer representation.
#     max_len : int
#         Maximum number of words to be in a sequence. They can be either padded or truncated based on the max_len.
#     padding : str
#         A string specifying the weather the padding can be 'pre' or 'post'. 
#     binary_label: bool
#         Weather the labels are for binary classification or not.

#     Returns
#     -------
#     values: tuple
#         A tuple of label to feature tensor pairs.

#     See Also
#     --------
#     label_pipeline: Convert string label to an integer representation of that label.
#     text_pipeline: Converts sentence to tokens of integers.
    
#     Examples
#     --------
#     >>> vocab = {'<unk>': 0, 'this': 1, 'is': 2, 'a': 3, 'dog': 4}
#     >>> tokenizer = lambda x: x.split(' ')
#     >>> print(text_pipeline("This is a dog that is backing", tokenizer=tokenizer, vocab=vocab, unk_token='<unk>', lower=True))
#     [1, 2, 3, 4, 0, 2, 0]
#     """
    
#     assert padding=="pre" or padding=="post", "the padding can be either pre or post"
#     labels_list, text_list = [], []
#     for _label, _text in batch:
#         labels_list.append(label_pipeline(_label))
#         text_holder = torch.zeros(max_len, dtype=torch.int32) # fixed size tensor of max_len with <pad> = 0
#         processed_text = torch.tensor(text_pipeline(_text), dtype=torch.int32)
#         pos = min(max_len, len(processed_text))
#         if padding == "pre":
#             text_holder[:pos] = processed_text[:pos]
#         else:
#             text_holder[-pos:] = processed_text[-pos:]
#         text_list.append(text_holder.unsqueeze(dim=0))
#     return torch.FloatTensor(labels_list) if binary_label else torch.LongTensor(labels_list), torch.cat(text_list, dim=0)



