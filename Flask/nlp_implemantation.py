from gingerit.gingerit import GingerIt
import truecase
import spacy
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from nltk.corpus import wordnet
import ChatMate  


def autospell_corrector(text):
    parser = GingerIt()
    corrected_text = parser.parse(text)['result']
    
    final_text = truecase.get_true_case(corrected_text)
    
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(final_text)
    
    if not doc[-1].text.endswith('?') and not any(token.tag_ == 'WDT' for token in doc):
        if doc[-1].text not in ['.', '!']:
            if doc[-1].is_sent_start:
                corrected_text += '.'
            elif doc[-1].is_title:
                corrected_text += '.'
            elif doc[-1].is_quote:
                corrected_text += '.'
            elif doc[-1].pos_ in ['NOUN', 'PROPN', 'VERB', 'ADJ', 'ADV']:
                corrected_text += '.'
    
    return corrected_text

def NER(sentence):
    tokens = word_tokenize(sentence)
    tagged_tokens = pos_tag(tokens)
    entities = ne_chunk(tagged_tokens)
    names = []
    for entity in entities:
        if hasattr(entity, 'label'):
            name = ' '.join(c[0] for c in entity)
            names.append(name)
            gender = ChatMate.predict_gender(name)
            ChatMate.create_Node(name,gender)
            print('Entity:', ' '.join(c[0] for c in entity), 'Type:', entity.label())
    print(names)


#Wordnet Implement
def get_word_definition(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return "No definition found for '{}'.".format(word)
    definition = synsets[0].definition()
    return definition.capitalize()

