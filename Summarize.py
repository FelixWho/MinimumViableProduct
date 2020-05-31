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

print("Setting up SpaCy large (lg) english corpus...")
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe(nlp.create_pipe('sentencizer'))

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
    doc = nlp(text.lower())
    sentences = [re.sub(r'[^a-zA-Z]', ' ', expandContractions(sent.text)).strip() for sent in doc.sents]
    sentences = list(filter(None, sentences))
    
    ret = [post_process_text(x) for x in sentences]

    return ret

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

def main():
    top_n = 2
    text="In an attempt to build an AI-ready workforce, Microsoft announced Intelligent Cloud Hub which has been launched to empower the next generation of students with AI-ready skills. Envisioned as a three-year collaborative program, Intelligent Cloud Hub will support around 100 institutions with AI infrastructure, course content and curriculum, developer support, development tools and give students access to cloud and AI services. As part of the program, the Redmond giant which wants to expand its reach and is planning to build a strong developer ecosystem in India with the program will set up the core AI infrastructure and IoT Hub for the selected campuses. The company will provide AI development tools and Azure AI services such as Microsoft Cognitive Services, Bot Services and Azure Machine Learning.According to Manish Prakash, Country General Manager-PS, Health and Education, Microsoft India, said, \"With AI being the defining technology of our time, it is transforming lives and industry and the jobs of tomorrow will require a different skillset. This will require more collaborations and training and working with AI. That’s why it has become more critical than ever for educational institutions to integrate new cloud and AI technologies. The program is an attempt to ramp up the institutional set-up and build capabilities among the educators to educate the workforce of tomorrow.\" The program aims to build up the cognitive skills and in-depth understanding of developing intelligent cloud connected solutions for applications across industry. Earlier in April this year, the company announced Microsoft Professional Program In AI as a learning track open to the public. The program was developed to provide job ready skills to programmers who wanted to hone their skills in AI and data science with a series of online courses which featured hands-on labs and expert instructors as well. This program also included developer-focused AI school that provided a bunch of assets to help build AI skills."
    
    sentences = normalizeSentences(text)
    print("Cleaning sentences")

    similarity_matrix = calc_similarity(sentences)
    print("Calculate sentence cross-similarity")

    sentence_similarity_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)
    print("Page rank sentences")

    summarized_text = []
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    #print("Indexes of top ranked_sentence order are ", ranked_sentence)
    for i in range(top_n):
        summarized_text.append(" ".join(ranked_sentence[i][1]))
    
    #print("Summarize Text: \n", ". ".join(summarized_text))

if __name__=="__main__": 
    main()