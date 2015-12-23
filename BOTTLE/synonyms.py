import sys
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

def get_synonyms(word):
    syns = []
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            syns.append(lemma.name())
    return(syns)

def get_custom_synonyms(word):
    syns = []
    if word == 'animal':
        syns = ['dog', 'cat', 'pet', 'wildlife']
    elif word == 'arts': 
        syns = ['garden', 'film', 'society', 'poetry', 'festival', 'guild']
    elif word == 'children':
        syns = ['childhood', 'child', 'student', 'youth', 'boys', 'girls', 'brothers', 'sisters']
    elif word == 'disaster':
        syns = ['relief', 'hurricane', 'earthquake', 'tsunami']
    elif word == 'education':
        syns = ['graduate', 'graduation', 'scholarship', 'scholar', 'mentor', 'mentoring']
    elif word == 'environment':
        syns = ['climate', 'planet', 'leed', 'green', 'natural', 'earth']
    elif word == 'health':
        syns = ['runners', 'running', 'marathon', 'race', 'cancer', 'diabetes', 'research', 'cure', 'hospital']
    return(syns)
