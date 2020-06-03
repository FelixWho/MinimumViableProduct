# deeppavlov
from deeppavlov import build_model
from deeppavlov import train_model

from tensorflow import keras
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import json

import EntityRecognizer

cnn_config = { "dataset_reader": { "class_name": "basic_classification_reader", "x": "Text", "y": "Intent", "data_path": "./Raw Data/", "train": "train.csv" }, "dataset_iterator": { "class_name": "basic_classification_iterator", "seed": 42, "split_seed": 23, "field_to_split": "train", "split_fields": [ "train", "valid" ], "split_proportions": [ 0.8, 0.2 ] }, "chainer": { "in": [ "x" ], "in_y": [ "y" ], "pipe": [ { "id": "classes_vocab", "class_name": "simple_vocab", "fit_on": [ "y" ], "level": "token", "save_path": "./tmp/classes.dict", "load_path": "./tmp/classes.dict", "in": "y", "out": "y_ids" }, { "in": "x", "out": "x_tok", "id": "my_tokenizer", "class_name": "nltk_tokenizer", "tokenizer": "wordpunct_tokenize" }, { "in": "x_tok", "out": "x_emb", "id": "my_embedder", "class_name": "glove", "load_path": "./glove.6B.100d.txt", "dim": 100, "pad_zero": True }, { "in": "y_ids", "out": "y_onehot", "class_name": "one_hotter", "depth": "#classes_vocab.len", "single_vector": True }, { "in": [ "x_emb" ], "in_y": [ "y_onehot" ], "out": [ "y_pred_probas" ], "main": True, "class_name": "keras_classification_model", "save_path": "./cnn_model_v1", "load_path": "./cnn_model_v1", "embedding_size": "#my_embedder.dim", "n_classes": "#classes_vocab.len", "kernel_sizes_cnn": [ 1, 2, 3 ], "filters_cnn": 256, "optimizer": "Adam", "learning_rate": 0.01, "learning_rate_decay": 0.1, "loss": "categorical_crossentropy", "coef_reg_cnn": 1e-4, "coef_reg_den": 1e-4, "dropout_rate": 0.5, "dense_size": 100, "model_name": "cnn_model" }, { "in": "y_pred_probas", "out": "y_pred_ids", "class_name": "proba2labels", "max_proba": True }, { "in": "y_pred_ids", "out": "y_pred_labels", "ref": "classes_vocab" } ], "out": [ "y_pred_labels" ] }, "train": { "epochs": 10, "batch_size": 64, "metrics": [ "sets_accuracy", "f1_macro", { "name": "roc_auc", "inputs": ["y_onehot", "y_pred_probas"] } ], "validation_patience": 5, "val_every_n_epochs": 1, "log_every_n_epochs": 1, "show_examples": True, "validate_best": True, "test_best": False } }

m = build_model(cnn_config)

def getResult(query):
    looking_for = m([query])[0]
    disease = EntityRecognizer.recognize(query)[0]

    dict_equiv = {"Treatment": "treatment_simple", "Symptom":"symptoms_description", "ShortDescription": "description_short","LongDescription": "description_long","Infectiousness": "infectiousness","Cause" : "cause", "Prevention": "prevention", "Screening":"screening"}

    with open('./database_with_mayo_and_medline_links.txt') as jsonfile:
        data = json.load(jsonfile)
    data = data[disease][dict_equiv[looking_for]]
    resp = ""
    if looking_for == "Infectiousness" and data:
      resp = disease + " is spread "
      for i in range(len(data)):
        resp+=str(i+1)+") "+data[i] + " "
      resp = resp.strip()
    else:
      resp = data

    return resp

# test
#query1 = "What are symptoms of Addisons disease?"
#query2 = "How to spread chlamydia?"
#print(getResult(query1))
#print(getResult(query2))
