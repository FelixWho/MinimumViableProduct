from itertools import islice
import re
import spacy
import pkg_resources
from symspellpy import SymSpell

# SpaCy English model 
# Possibly can change to 'sm, md, lg, ...'
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(nlp.create_pipe('sentencizer'))

# SymSpell word correction tool
# Fixes text messages that contain poor grammar/spelling
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
bigram_path = pkg_resources.resource_filename("symspellpy", "frequency_bigramdictionary_en_243_342.txt")
sym_spell.load_dictionary(dictionary_path, 0, 1)
sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)

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
    par = nlp(sentence)

    if par[len(par)-1].text == "?":
        return True
    first_word = par[0].text.lower()
    if first_word in question_beginners:
        return True
    return False

def main():
    # Sample text message
    #text_message = "What is HIV testing? Who's Felix, etc.? what's going on? Multiple sentences."
    #text_message = "What is HIV?"
    #text_message = "hiv?"
    #text_message = "myheadisHIV?"
    #text_message = "mynameisFelixwhat'syours?"
    #text_message = "Where can I get tested for HIV?"
    #text_message = "What are symptoms of HIV?"
    text_message = "Whatare symptomsof HIV? Hi my name is Felix Hu!"
    #text_message = "."
    #text_message = "symptoms of HIV"
    #text_message = "What does hiv mean?"
    #text_message = "Can you pick out natural language processing?"

    # Preprocessing text
    text_message_orig = text_message # preserve original
    #text_message_f = text_message.lower() # lowercase
    text_message_f = expandContractions(text_message) # expand contractions

    # Feed to SpaCy
    doc = nlp(text_message_f)

    # Split by sentences
    sentences = [sent.string.strip() for sent in doc.sents]

    text_message_seg = [sym_spell.lookup_compound(sentence[:1].lower() + sentence[1:], max_edit_distance=2,
                                            transfer_casing=True) for sentence in sentences]
    print(sentences)
    for suggestions in text_message_seg:
        for s in suggestions:
            print(s)

    for sent in sentences:
        if not isQuestion(text_message_orig):
            continue
        # Pick out subject and possessed quality. Symptoms of HIV --> HIV's symptoms.


if __name__=="__main__": 
    main()