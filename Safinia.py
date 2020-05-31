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
sym_spell = SymSpell(max_dictionary_edit_distance=0, prefix_length=7)
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

def correctGrammarSpelling(sentence):
    # More rigorous check would be sym_spell.lookup_compound()
    return sym_spell.word_segmentation(sentence[:1].lower() + sentence[1:]).corrected_string

def main():
    # Sample text message
    #text_message = "What is HIV testing? Who's Felix, etc.? what's going on? Multiple sentences."
    #text_message = "What is HIV?"
    #text_message = "hiv?"
    #text_message = "myheadisHIV?"
    #text_message = "mynameisFelixwhat'syours?"
    #text_message = "Where can I get tested for HIV?"
    #text_message = "What are symptoms of HIV?"
    #text_message = "Whatare symptomsof HIV? Hi my name is Felix Hu!"
    #text_message = "whereis th elove hehad dated forImuch of thepast who "
    text_message = "What are symptoms of hiv?"
    #text_message = "HIV's symptoms"
    #text_message = "Conor's dog's toy was hidden under the man's sofa in the woman's house"

    # Preprocessing text
    text_message_orig = text_message # preserve original
    #text_message_f = text_message.lower() # lowercase
    text_message_f = expandContractions(text_message) # expand contractions

    # Feed to SpaCy
    doc = nlp(text_message_orig)

    # Split by sentences
    sentences = [sent.string.strip() for sent in doc.sents]

    # TODO BUG Correct grammar/spelling errors
    # We attempt to use SymSpell to correct errors.
    # Issues:
    #   1) Complex medical terms are usually changed
    #   2) Seemingly not consistent 
    #sentences_segmented = [correctGrammarSpelling(sentence) for sentence in sentences]
    #for suggested in sentences_segmented:
    #    print(suggested)

    print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])


if __name__=="__main__": 
    main()