import spacy
from spacy.tokens import Doc
import spacy
nlp = spacy.load('en_core_web_lg')

class WhitespaceTokenizer(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = text.split(' ')
        # All tokens 'own' a subsequent space character in this tokenizer
        spaces = [True] * len(words)
        return Doc(self.vocab, words=words, spaces=spaces)
nlp.tokenizer = WhitespaceTokenizer(nlp.vocab)



def diff2before_after_taglook(text , tag):
    before, after , tmp_V = [], [] ,[]
    for token in text.split(' '):
        if token.startswith('{+'):
            after_word = token[2:-2].split('//')[0].replace('\u3000',' ')
            t = token[2:-2].split('//')[1]
            if t==tag:
                after.append(token)
                tmp_V.append(token)
            else:
                after.append(after_word)
        elif token.startswith('[-'):
            if token.endswith('+}'):
                delete_tmp, insert_tmp = token[2:-2].split('-]{+')
                delete = delete_tmp.split('//')[0].replace('\u3000',' ')
                insert = insert_tmp.split('//')[0].replace('\u3000',' ')
                t = insert_tmp.split('//')[1]
                if t==tag:
                    before.append(token)
                    after.append(token)
                    tmp_V.append((token))
                else:
                    before.append(delete)
                    after.append(insert)
            else:
                before_word = token[2:-2].split('//')[0].replace('\u3000',' ')
                t = token[2:-2].split('//')[1]
                if t==tag:
                    before.append(token)
                    tmp_V.append(token)
                else:
                    before.append(before_word)
        else:
            toke = token.replace('\u3000',' ')
            before.append(token)
            after.append(token)
    return  ' '.join(after) , tmp_V


def diff_after_before(text):
    before, after = [], []
    for token in text.split(' '):
        if token.startswith('{+'):
            after_word = token[2:-2].split('//')[0]
            after.append(after_word)
        elif token.startswith('[-'):
            if token.endswith('+}'):
                delete_tmp, insert_tmp = token[2:-2].split('-]{+')
                delete = delete_tmp.split('//')[0]
                insert = insert_tmp.split('//')[0]
                before.append(delete)
                after.append(insert)
            else:
                before_word = token[2:-2].split('//')[0]
                before.append(before_word)
        else:
            before.append(token)
            after.append(token)
    return ' '.join(before).replace('\u3000',' '), ' '.join(after).replace('\u3000',' ')




def find_segment(tag_sen , tag_arry):
    
    def find_seg_index(token):
        l = len(token)
        seg_index_tmp=[]
        for index, word in enumerate(token):
            if 'VT' in word:
                seg_index_tmp.append((index-1,index,index+1))
        seg_ngram_index = []
        for ii in seg_index_tmp:
            seg_index = []
            for i in ii:
                if i<0:
                    seg_index.append(0)
                elif i>=l:
                    seg_index.append(l-1)
                else:
                    seg_index.append(i)
            seg_index = sorted(set(seg_index))
            seg_ngram_index.append(seg_index)
        return seg_ngram_index
    
    token = tag_sen.split(' ')
    index_arry = find_seg_index(token)
    segment_arry = []
    for index , tag in zip(index_arry , tag_arry):
        seg = ' '.join([token[i] for i in index])
        before , after = diff_after_before(seg)
        segment_arry.append((before , after))
    return segment_arry

def spacy_index_match(sen , index):
    all_tag = ['VBP' , 'VBZ' , 'VBG' , 'VBN' , 'VBD' , 'VB']
    word = ['will']
    doc = nlp(sen)
    show = []
    for i in index:
        if doc[i].text in word or doc[i].tag_ in all_tag:
            show.append((doc[i].text , doc[i].tag_))
    return show

def find_segment_position(full, part):
    full = full.split()
    part = part.split()
    length = len(part)
    for i, sublist in enumerate((full[i:i+length] for i in range(len(full)))):
        if part == sublist:
            return [i+c for c in range(length)]
    return []

def find_pattern_spacy_result(sen ,pattern='VT'):
    tag_sen , tag = diff2before_after_taglook(sen , pattern)
    before , after = diff_after_before(tag_sen)
    before  = ' '.join([i for i in before.split(' ') if i])
    after = ' '.join([i for i in after.split(' ') if i])
    segment_arry = find_segment(tag_sen , tag)
    result = []
    for segment in segment_arry:
        before_seg = segment[0]
        after_seg = segment[1]
        b_index = find_segment_position(before , before_seg)
        a_index = find_segment_position(after , after_seg)
        b_spacy_result = spacy_index_match( before , b_index)
        a_spacy_result = spacy_index_match( after , a_index)
        result.append((b_spacy_result , a_spacy_result))
        #print(b_spacy_result , a_spacy_result)
    return result , tag_sen

from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
def pair_key(pair):
    key_verb =''
    before_word = [lemmatizer(i[0] , 'VERB')[0] for i in pair[0]]
    after_word = [lemmatizer(i[0] , 'VERB')[0] for i in pair[1]]
    #print(before_word , after_word)
    #list3 = set(before_word)&set(after_word)
    #list4 = sorted(list3, key = lambda k : before_word.index(k))
    return after_word[-1] 

