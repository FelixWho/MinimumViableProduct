# pip install -U spacy
# python -m spacy download en_core_web_sm

import re
import spacy

# English model, possibly can change ('sm, md, lg, ...')
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(nlp.create_pipe('sentencizer'))

def expandContractions(phrase):
    '''
    Simplified version of expanding common English contractions.
    '''
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

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

doc = nlp(text_message_dec)

# Analyze syntax, wording
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Sentences: ", [sent.string.strip() for sent in doc.sents])