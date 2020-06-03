import nltk
from symspellpy import SymSpell, Verbosity
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
sym_spell = SymSpell()
sym_spell.load_dictionary('disease_dict', 0, 1, separator="$")
def recognize(query_text):
  sent = nltk.word_tokenize(query_text)
  pos_tag = nltk.pos_tag(sent)
  disease_pattern = r"""
                DISEASE: {(<NN.*><POS>){0,1}<JJ>*<NN.*>+(<IN><DT><NN.*>+){0,1}}                           
              """
  cp = nltk.RegexpParser(disease_pattern)
  ret = []
  for chunk in cp.parse(pos_tag).subtrees():
    if chunk.label() == 'DISEASE':
      buf = ""
      for word in chunk:
        if word[1] != 'POS':
          buf += ' '
        buf += word[0]
      suggestions = sym_spell.lookup(buf.strip().lower(), Verbosity.CLOSEST,
                               max_edit_distance=2)
      ret.extend([x._term for x in suggestions])
  return ret
