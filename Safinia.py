# pip install -U spacy
# python -m spacy download en_core_web_sm

import re
import spacy

# English model, possibly can change ('sm, md, lg, ...')
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(nlp.create_pipe('sentencizer'))

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

def isQuestion(sentence):
    '''
    Return boolean on whether the sentence is a question or not
    Metrics: contains "?"/starts with keyword
    '''
    question_beginners = ["is", "does", "do", "what", "when", "where", "who", "why", "what", "how"]
    
    sentence = sentence.strip() # remove beginning/end whitespace
    doc = nlp(sentence)

    if doc[len(doc)-1].is_punct:
        return True
    first_word = doc[0].text.lower()
    if first_word in question_beginners:
        return True
    return False

# Sample text message
#text_message = "What is HIV testing? Who's Felix, etc.? what's going on?"
text_message = "What is HIV?"
#text_message = "Where can I get tested for HIV?"
#text_message = "What are symptoms of HIV?"
#text_message = "symptoms of HIV"

# Expand contractions
text_message_dec = expandContractions(text_message)

# Feed to SpaCy
doc = nlp(text_message_dec)

# Analyze syntax, wording
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Sentences: ", [sent.string.strip() for sent in doc.sents])