# deeppavlov
from deeppavlov.dataset_readers.basic_classification_reader import BasicClassificationDatasetReader
from deeppavlov.dataset_iterators.basic_classification_iterator import BasicClassificationDatasetIterator
from deeppavlov.models.preprocessors.str_lower import str_lower
from deeppavlov.models.tokenizers.nltk_moses_tokenizer import NLTKMosesTokenizer
from deeppavlov.core.data.simple_vocab import SimpleVocabulary
from deeppavlov.models.embedders.bow_embedder import BoWEmbedder
from deeppavlov.core.data.utils import simple_download
from deeppavlov.models.embedders.glove_embedder import GloVeEmbedder
from deeppavlov.metrics.accuracy import sets_accuracy
from deeppavlov.models.classifiers.keras_classification_model import KerasClassificationModel
from deeppavlov.models.preprocessors.one_hotter import OneHotter
from deeppavlov.models.classifiers.proba2labels import Proba2Labels
from deeppavlov import build_model
from deeppavlov import train_model

from tensorflow import keras
import os
import numpy as np 
import pandas as pd
from tqdm import tqdm
import os.path

# Get data from columns of intents.csv file
dr = BasicClassificationDatasetReader().read(
    data_path='./Raw Data/',
    train='train.csv',
    x = 'Text',
    y = 'Intent',
    header = 0,
    sep = ',',
    names = ["Text", "Intent"]
)

# initialize data iterator splitting `train` field to `train` and `valid` in proportion 0.8/0.2
train_iterator = BasicClassificationDatasetIterator(
    data=dr,
    field_to_split='train',  # field that will be splitted
    split_fields=['train', 'valid'],   # fields to which the fiald above will be splitted
    split_proportions=[0.8, 0.2],  #proportions for splitting
    split_seed=121,  # seed for splitting dataset
    seed=21)  # seed for iteration over dataset

#print([(k, len(dr[k])) for k in dr.keys()])

# print a few x, y pairs
x_train, y_train = train_iterator.get_instances(data_type='train')
for x, y in list(zip(x_train, y_train))[:3]:
    print('x:', x)
    print('y:', y)
    print('=================')

# tokenize all input data
tokenizer = NLTKMosesTokenizer()
train_x_lower_tokenized = str_lower(
                          tokenizer(
                          train_iterator.get_instances(data_type='train')[0]
                          ))

# get the intent categories
classes_vocab = SimpleVocabulary(save_path='./tmp/classes.dict',
                                 load_path='./tmp/classes.dict')
classes_vocab.fit(train_iterator.get_instances(data_type='train')[1])
classes_vocab.save()
print(list(classes_vocab.items())) # display classes

# get all token vocab
token_vocab = SimpleVocabulary(save_path='./tmp/tokens.dict',
                               load_path='./tmp/tokens.dict')
token_vocab.fit(train_x_lower_tokenized)
token_vocab.save()

# we will use GLOVE embedding
if not os.path.isfile("./glove.6B.100d.txt"):
    simple_download(url="http://files.deeppavlov.ai/embeddings/glove.6B.100d.txt", destination="./glove.6B.100d.txt")
embedder = GloVeEmbedder(load_path='./glove.6B.100d.txt',dim=100, pad_zero=True)

x_train, y_train = train_iterator.get_instances(data_type="train")
x_valid, y_valid = train_iterator.get_instances(data_type="valid")

cls = KerasClassificationModel(save_path="./cnn_model_v0", 
                               load_path="./cnn_model_v0", 
                               embedding_size=embedder.dim,
                               n_classes=classes_vocab.len,
                               model_name="cnn_model",
                               text_size=15, # number of tokens
                               kernel_sizes_cnn=[3, 5, 7],
                               filters_cnn=128,
                               dense_size=100,
                               optimizer="Adam",
                               learning_rate=0.1,
                               learning_rate_decay=0.01,
                               loss="categorical_crossentropy")

onehotter = OneHotter(depth=classes_vocab.len, single_vector=True)

# epochs
for ep in range(10):
    for x, y in tqdm(train_iterator.gen_batches(batch_size=64, 
                                           data_type="train")):
        x_embed = embedder(tokenizer(str_lower(x)))
        y_onehot = onehotter(classes_vocab(y))
        cls.train_on_batch(x_embed, y_onehot)

cls.save()

print(embedder(tokenizer(str_lower(x_valid))))
#prob2labels = Proba2Labels(max_proba=True)

"""
print("Text sample: {}".format(x_valid[0]))
print("True label: {}".format(y_valid[0]))
print("Predicted probability distribution: {}".format(dict(zip(classes_vocab.keys(), 
                                                               y_valid_pred[0]))))
print("Predicted label: {}".format(classes_vocab(prob2labels(y_valid_pred))[0]))

print(sets_accuracy(y_valid, classes_vocab(prob2labels(y_valid_pred))))
"""
# JSON CONFIGURATION SETTINGS -- NOT USED

"""
conf = {"dataset_reader": {
    "class_name": "basic_classification_reader",
    "x": "Text",
    "y": "Intent",
    "data_path": "./Raw Data/",
    "train": "train.csv"
    },
    "dataset_iterator": {
    "class_name": "basic_classification_iterator",
    "seed": 123,
    "split_seed": 456,
    "field_to_split": "train",
    "split_fields": [
        "train",
        "valid"
    ],
    "split_proportions": [0.9,0.1]
  },
  "chainer": {
    "in": ["x"],
    "in_y": ["y"],
    "pipe": [
        {
        "id": "classes_vocab",
        "class_name": "simple_vocab",
        "fit_on": ["y"],
        "save_path": "./Question/classes.dict",
        "load_path": "./Question/classes.dict",
        "in": "y",
        "out": "y_ids"
        },
        {
        "in": ["x"],
        "out": ["x_vec"],
        "fit_on": ["x","y_ids"],
        "id": "tfidf_vec",
        "class_name": "sklearn_component",
        "save_path": "tfidf_v1.pkl",
        "load_path": "tfidf_v1.pkl",
        "model_class": "sklearn.feature_extraction.text:TfidfVectorizer",
        "infer_method": "transform"
        },
        {
        "in": "x",
        "out": "x_tok",
        "id": "my_tokenizer",
        "class_name": "nltk_moses_tokenizer",
        "tokenizer": "wordpunct_tokenize"
        },
        {
        "in": ["x_vec"],
        "out": ["y_pred"],
        "fit_on": ["x_vec","y"],
        "class_name": "sklearn_component",
        "main": True,
        "save_path": "logreg_v2.pkl",
        "load_path": "logreg_v2.pkl",
        "model_class": "sklearn.linear_model:LogisticRegression",
        "infer_method": "predict",
        "ensure_list_output": True
        }
    ],
    "out": ["y_pred"]
    },
    "train": {
    "batch_size": 64,
    "metrics": ["accuracy"],
    "validate_best": True,
    "test_best": False
    }
}

#m = train_model(conf)
m = build_model(conf)
m(["What is HIV?"])
"""