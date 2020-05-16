# MinimumViableProduct
MVP for Core Safinia Functionality

# Resources

- https://github.com/wolfgarbe/SymSpell/blob/master/README.md
- https://www.mayoclinic.org/diseases-conditions
- https://spacy.io/universe/project/spacy_hunspell

# Pipeline

Twilio SMS --> MVP Script --> split by sentences --> correct minor spelling

--> figure out subject of question using SpaCy parts of speech ("What are symptoms of HIV" --> ["HIV", "Symptoms"])

--> find appropriate heading in Mayo Clinic website --> return query

# Requirements

    pip install -U spacy
    python -m spacy download en_core_web_sm
