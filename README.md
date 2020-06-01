# MinimumViableProduct
MVP for Core Safinia Functionality

# Resources

- https://github.com/wolfgarbe/SymSpell/blob/master/README.md
- https://www.mayoclinic.org/diseases-conditions
- https://spacy.io/universe/project/spacy_hunspell
- https://cs.pomona.edu/~dkauchak/simplification/
- https://github.com/miso-belica/sumy
- https://github.com/XingxingZhang/pysari
- https://github.com/deepmipt/DeepPavlov
- WikiLarge/WikiSmall datasets
- https://nlpforhackers.io/libraries/ #lists NLP libraries
- https://www.aclweb.org/anthology/W14-1207.pdf #medical text simplification using synonym replacement
- https://www.grammarly.com/blog/engineering/plainly-speaking-a-linguistic-approach-to-simplifying-complex-words/
- https://github.com/deepmipt/DeepPavlov/blob/master/examples/classification_tutorial.ipynb
- https://www.kaggle.com/kageyama/deeppavlov-news-category-classification

# Pipeline

Twilio SMS --> MVP Script --> split by sentences --> correct minor spelling

--> figure out subject of question using SpaCy parts of speech ("What are symptoms of HIV" --> ["HIV", "Symptoms"])

--> find appropriate heading in Mayo Clinic website --> return query

# Safinia.py

Takes in text message. Splits message into sentences using SpaCy. Corrects sentence grammer/spelling with SymSpell. Determine if sentence is question or not.

# Database Intents

- Description
- Symptoms
- Testing Methodology
- Treatment Options, Average Cost of Treatment
- Cause
- Infectiousness (how it's spread)
- Risk Factors
- Prevention Measures

### Steps to train intent model with deeppavlov

Be sure to delete any pre-existing models beforehand.

    python IntentTrainingDataBuilder.py # writes to train.csv file in Raw Data
    python IntentTrainerUsingConfig.py # train using configuration
    python IntentLoader.py # build the model back up

# Requirements

    pip install -U spacy
    python -m spacy download en_core_web_sm
    python -m spacy download en_core_web_lg # possible read timeout
    pip install beautifulsoup4
    python -m pip install -U symspellpy
    pip install deeppavlov
    pip install gensim
    pip install networkx
    pip install textstat
