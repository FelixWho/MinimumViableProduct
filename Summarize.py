# partial credit to: https://towardsdatascience.com/understand-text-summarization-and-create-your-own-summarizer-in-python-b26a9f09fc70
# for motivation
# returns the top_n important sentences

from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import spacy
import re
import textstat

print("Setting up SpaCy large (lg) english corpus (Summarize.py)...")
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe(nlp.create_pipe('sentencizer'), before="parser")

def break_sentences(text): 
    doc = nlp(text)
    return doc.sents

def word_count(text): 
    sentences = break_sentences(text) 
    words = 0
    for sentence in sentences: 
        words += len([token for token in sentence]) 
    return words 

def avg_sentence_length(text): 
    words = word_count(text) 
    sentences = textstat.sentence_count(text)
    average_sentence_length = float(words / sentences) 
    return average_sentence_length


def expandContractions(sentence):
    '''
    Simplified version of expanding common English contractions.
    '''
    # specific
    sentence = re.sub(r"won\'t", "will not", sentence)
    sentence = re.sub(r"can\'t", "can not", sentence)
    # general
    sentence = re.sub(r"n\'t", " not", sentence)
    sentence = re.sub(r"\'re", " are", sentence)
    sentence = re.sub(r"\'s", " is", sentence)
    sentence = re.sub(r"\'d", " would", sentence)
    sentence = re.sub(r"\'ll", " will", sentence)
    sentence = re.sub(r"\'t", " not", sentence)
    sentence = re.sub(r"\'ve", " have", sentence)
    sentence = re.sub(r"\'m", " am", sentence)
    return sentence

def normalizeSentences(text):
    doc = nlp(text)
    sentences = [re.sub(r'[^a-zA-Z]', ' ', expandContractions(sent.text)).strip().lower() for sent in doc.sents]
    sentences = list(filter(None, sentences))
    
    ret1 = [post_process_text(x) for x in sentences]

    return (ret1, [sent.text for sent in doc.sents])

def post_process_text(text):
    '''
    https://medium.com/better-programming/the-beginners-guide-to-similarity-matching-using-spacy-782fc2922f7c
    '''
    text = ' '.join(text.split()) # turn multiple whitespace to single whitespace
    doc = nlp(text)
    result = []
    for token in doc:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.lemma_ == '-PRON-':
            continue
        result.append(token.lemma_)
    return " ".join(result)

def calc_similarity(sentences):
    '''
    Calculate similarity between all pairs sentences.
    '''
    similarity_matrix = np.ones((len(sentences), len(sentences)))
    docs = [nlp(x) for x in sentences]
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            a = docs[idx1]
            b = docs[idx2]
            similarity_matrix[idx1][idx2] = a.similarity(b)
    return similarity_matrix

def shorten(text, ratio):
    
    obj = normalizeSentences(text)
    sentences = obj[0]
    orig_sentences = obj[1]
    #print("Cleaning sentences")
    #print(orig_sentences)
    
    top_n = int(ratio*len(orig_sentences))

    similarity_matrix = calc_similarity(sentences)
    #print("Calculate sentence cross-similarity")

    sentence_similarity_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)
    #print("Page rank sentences")
    #print(scores)

    summarized_text = ""
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(orig_sentences)), reverse=True)
    #print(ranked_sentence)

    #print("Indexes of top ranked_sentence order are ", ranked_sentence)
    for i in range(top_n):
        summarized_text += ranked_sentence[i][1]+" "
    
    summarized_text = summarized_text.strip()

    return summarized_text
